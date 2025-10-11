from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, Line, Rectangle

MENU_ITEMS = ["たたかう","スキル","アイテム","にげる"]

def hex_to_rgba(h, a=1.0):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4)) + (a,)

class BattleScreen(Screen):
    def __init__(self, director, **kwargs):
        super().__init__(**kwargs)
        self.director = director
        self._keyboard=None; self._blink=False; self._blink_ev=None
        self.menu_labels=[]; self.info_top=None; self.info_bottom=None
        self.cards=[]; self.enemy_slots=[]

    def on_pre_enter(self,*args):
        self.director.start_battle()
        self._ensure_keyboard(); self._build_ui(); self._update_all()
        if not self._blink_ev: self._blink_ev = Clock.schedule_interval(self._tick_blink, 0.5)

    def on_leave(self,*args):
        self._release_keyboard(); 
        if self._blink_ev: self._blink_ev.cancel(); self._blink_ev=None

    def _build_ui(self):
        theme=self.director.theme; battle=theme.get("battle",{}); pal=theme.get("palette",{})
        self.clear_widgets()
        root = MDBoxLayout(orientation="vertical", padding=6, spacing=6)

        if battle.get("message_top_panel", False):
            top = MDCard(orientation="vertical", padding=6, size_hint_y=None, height=40)
            self.info_top = MDLabel(text="コマンドを選択してください", halign="center")
            top.add_widget(self.info_top); root.add_widget(top)

        mid = MDBoxLayout(orientation="horizontal", spacing=6)
        enemies_area = MDCard(orientation="vertical", padding=6)
        enemies_grid = MDGridLayout(cols=3, spacing=6)
        self.enemy_slots=[]
        for idx, e in enumerate(self.director.enemies):
            slot = MDCard(orientation="vertical", padding=4, size_hint=(1,1))
            label = MDLabel(text=e["name"], halign="center")
            hp = MDLabel(text=f"HP:{e['hp']}/{e['hp_max']}", halign="center")
            slot.add_widget(label); slot.add_widget(hp)
            self.enemy_slots.append((slot,label,hp)); enemies_grid.add_widget(slot)
        enemies_area.add_widget(enemies_grid); mid.add_widget(enemies_area)

        party_area = MDCard(orientation="vertical", padding=6)
        cols = 2 if battle.get("menu_layout")=="horizontal-bottom" else 4
        bar = MDGridLayout(cols=cols, spacing=6, size_hint_y=None, height=160)
        self.cards=[]
        for p in self.director.party:
            card=MDCard(orientation="vertical", padding=6, radius=[10,10,10,10])
            card.add_widget(MDLabel(text=p["name"], font_style="Subtitle1"))
            if battle.get("status_style")=="bars":
                card.add_widget(self._make_bar("HP", p["hp"], p["hp_max"], pal.get("hp","#ef476f"), pal.get("panel","#222")))
                card.add_widget(self._make_bar("MP", p["mp"], p["mp_max"], pal.get("mp","#118ab2"), pal.get("panel","#222")))
            else:
                card.add_widget(MDLabel(text=f"HP: {p['hp']}/{p['hp_max']}", theme_text_color="Secondary"))
                card.add_widget(MDLabel(text=f"MP: {p['mp']}/{p['mp_max']}", theme_text_color="Secondary"))
            self.cards.append(card); bar.add_widget(card)
        party_area.add_widget(bar); mid.add_widget(party_area)
        root.add_widget(mid)

        bottom = MDCard(orientation="vertical", padding=6, size_hint_y=None, height=100)
        menu_bar = MDBoxLayout(orientation="horizontal" if battle.get("menu_layout")=="horizontal-bottom" else "vertical", spacing=12)
        self.menu_labels=[]
        for t in MENU_ITEMS:
            lbl = MDLabel(text=f"  {t}", halign="center", font_style="Subtitle1"); self.menu_labels.append(lbl); menu_bar.add_widget(lbl)
        info = MDLabel(text="", halign="left"); self.info_bottom = info
        bottom.add_widget(menu_bar); bottom.add_widget(info); root.add_widget(bottom)
        self.add_widget(root)

    def _make_bar(self, title, val, mx, color_hex, bg_hex):
        from kivymd.uix.boxlayout import MDBoxLayout
        box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=34, padding=2, spacing=2)
        box.add_widget(MDLabel(text=f"{title}: {val}/{mx}", theme_text_color="Secondary"))
        class Bar(MDBoxLayout):
            def __init__(self, val, mx, c_hex, bg_hex, **kw):
                super().__init__(**kw); self.val=val; self.mx=mx; self.c_hex=c_hex; self.bg_hex=bg_hex
                with self.canvas:
                    Color(*hex_to_rgba(bg_hex,1)); self.bg_rect = Rectangle()
                    Color(*hex_to_rgba(c_hex,1)); self.fg_rect = Rectangle()
                self.bind(pos=self._upd, size=self._upd)
            def _upd(self,*_):
                x,y = self.pos; w,h = self.size
                self.bg_rect.pos=(x,y); self.bg_rect.size=(w,h)
                ratio = max(0.0, min(1.0, self.val/self.mx if self.mx else 0))
                self.fg_rect.pos=(x,y); self.fg_rect.size=(w*ratio,h)
        bar = Bar(val, mx, color_hex, bg_hex, size_hint_y=None, height=12)
        box.add_widget(bar)
        return box

    def _draw_active_frames(self):
        idx=self.director.active_index; phase=self.director.phase
        for i,card in enumerate(self.cards):
            card.canvas.after.clear()
            with card.canvas.after:
                if phase in ('select','target') and i==idx:
                    a=1.0 if self._blink else 0.3
                    Color(1,0.9,0.2,a); Line(rectangle=(card.x,card.y,card.width,card.height), width=3)
                else:
                    Color(0.6,0.6,0.6,0.2); Line(rectangle=(card.x,card.y,card.width,card.height), width=1)
        for j,(slot,label,hp) in enumerate(self.enemy_slots):
            slot.canvas.after.clear()
            with slot.canvas.after:
                if self.director.phase=='target' and j==self.director.target_index:
                    a=1.0 if self._blink else 0.4
                    Color(0.9,0.8,0.2,a); Line(rectangle=(slot.x,slot.y,slot.width,slot.height), width=3)
                else:
                    Color(0.6,0.6,0.6,0.2); Line(rectangle=(slot.x,slot.y,slot.width,slot.height), width=1)

    def _update_menu_highlight(self):
        for i,lbl in enumerate(self.menu_labels):
            lbl.text = f"▶ {{}}".format(MENU_ITEMS[i]) if (i==self.director.menu_index and self.director.phase in ('select','target')) else f"  {{}}".format(MENU_ITEMS[i])

    def _update_messages(self):
        if self.director.phase=='select':
            n=self.director.party[self.director.active_index]['name']
            if self.info_top: self.info_top.text=f"{n} のコマンドを選んでください"
            if self.info_bottom: self.info_bottom.text=f"{n} の番です"
        elif self.director.phase=='target':
            e=self.director.enemies[self.director.target_index]['name']
            if self.info_top: self.info_top.text=f"ターゲットを選択：{e}"
            if self.info_bottom: self.info_bottom.text=f"←/→でメニュー、Tでターゲット変更、Enterで確定"
        else:
            s = " / ".join([f"{a['name']}:{a['cmd']}" + (f"→{a['target']}" if a['target'] else '') for a in self.director.selected_actions])
            if self.info_top: self.info_top.text="行動を実行しました（ダミー）"
            if self.info_bottom: self.info_bottom.text=s + "（Enterで次ターン／Escで終了）"

    def _update_all(self,*_):
        self._draw_active_frames(); self._update_menu_highlight(); self._update_messages()

    def _tick_blink(self,*_):
        self._blink=not self._blink; self._draw_active_frames()

    def _ensure_keyboard(self):
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            if self._keyboard: self._keyboard.bind(on_key_down=self._on_key_down)
    def _release_keyboard(self):
        if self._keyboard: self._keyboard.unbind(on_key_down=self._on_key_down); self._keyboard=None
    def _on_keyboard_closed(self): self._release_keyboard()

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1].lower()
        if key=='escape': self.manager.current='field'; return True
        if self.director.phase=='select':
            if key=='left': self.director.select_menu(-1); self._update_menu_highlight(); return True
            if key=='right': self.director.select_menu(+1); self._update_menu_highlight(); return True
            if key=='t': self.director.phase='target'; self._update_all(); return True
            if key in ('enter','kp_enter'):
                cmd = MENU_ITEMS[self.director.menu_index]
                self.director.confirm_selection(cmd); self._update_all(); return True
        elif self.director.phase=='target':
            if key in ('left','right','up','down'):
                step = -1 if key in ('left','up') else +1
                self.director.focus_next_target(step); self._draw_active_frames(); self._update_messages(); return True
            if key in ('enter','kp_enter'):
                cmd = MENU_ITEMS[self.director.menu_index]
                self.director.confirm_selection(cmd); self._update_all(); return True
        else:
            if key in ('enter','kp_enter'):
                self.director.reset_turn(); self._update_all(); return True
        return False