for n in range(1, 30):
    loop_counter = f"{n:02d}"
    print(f"{loop_counter}:", end='')  # カウンタだけ先に出す

    if n % 3 == 0:
        print("fizz", end='')

    if n % 5 == 0:
        print("bazz", end='')

    print()  # 行の最後で改行




# -*- coding: utf-8 -*-
"""
エラトステネスの篩（非再帰版）

【なぜ】
- 2〜n までの素数を、効率よく一気に列挙したい。
- 「素数の倍数を消していく」という発想で、無駄な割り算を減らす。

【前提】
- n は 2 以上の整数とする。（n < 2 のときは空リストを返す）
- Python のリストと for ループだけで実装する。

【入出力】
- 入力: n（int）… 素数を探す上限値。
- 出力: primes（list[int]）… 2〜n の中に含まれる素数一覧。

【副作用】
- 画面に出力はせず、戻り値としてリストを返すだけ。

【例外】
- n が 2 未満のときは、素数が存在しないので空リスト [] を返す。
"""

def sieve_iterative(n: int) -> list[int]:
    """エラトステネスの篩（非再帰版）で 2〜n の素数リストを返す。"""
    # --- 異常系や境界値の早期リターン ------------------------------
    if n < 2:
        # 2 未満には素数がないので、すぐに空リストを返す。
        return []

    # --- 真偽値リスト（is_prime）を準備 -----------------------------
    # インデックス i が「数 i」に対応するように、長さ n+1 のリストを用意する。
    # 最初は「すべて素数候補である」として True で初期化する。
    is_prime = [True] * (n + 1)

    # 0 と 1 は素数ではないので、あらかじめ False にしておく。
    is_prime[0] = False
    is_prime[1] = False

    # --- 篩（ふるい）処理のメイン部分 ------------------------------
    # ポイント：
    # - 素数候補 p は 2 からスタートする。
    # - p の最大は √n まで見れば十分。
    #   なぜなら、合成数 m は必ず「小さい方の因数」が √m 以下だから。
    import math
    limit = int(math.isqrt(n))  # n の平方根の整数部分

    for p in range(2, limit + 1):
        # すでに「素数ではない」と分かっている数は飛ばす。
        if not is_prime[p]:
            continue

        # ここに来た p は「素数」である。
        # この p の倍数をまとめて「素数ではない」とマークしていく。
        #
        # 開始位置を p*2 ではなく p*p からにする理由：
        # - 2p, 3p, ..., (p-1)p は、もっと小さい素数（2〜p-1）の篩で
        #   すでに消されているため。
        start = p * p

        # range(start, n+1, p) で p の倍数を順番にたどる。
        for multiple in range(start, n + 1, p):
            is_prime[multiple] = False

    # --- 結果の取り出し --------------------------------------------
    # is_prime[i] が True になっている i をすべて集めれば、それが素数リスト。
    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return primes


# 動作確認用の簡単なテスト
if __name__ == "__main__":
    N = 50
    primes_iter = sieve_iterative(N)
    print(f"[非再帰版] 2〜{N} の素数:", primes_iter)





# -*- coding: utf-8 -*-
"""
エラトステネスの篩（再帰版）

【ねらい】
- 「再帰関数」を使って、エラトステネスの篩の流れを別の角度から理解する。
- 外側の「p を 2,3,4,... と進めていく処理」と、
    内側の「p の倍数を順番に消していく処理」を、それぞれ再帰関数として分ける。

【前提】
- Python では再帰の最大深さに制限がある（デフォルト 1000 程度）。
- n が大きすぎる場合（数万や数十万など）は、再帰版では再帰深さ制限にかかる可能性がある。
    実用では非再帰版を使い、再帰版はあくまで教育用として扱う。

【入出力】
- 入力: n（int）
- 出力: primes（list[int]）

【副作用】
- 特になし（ただし、内部で is_prime リストを書き換える）

【例外】
- n < 2 の場合は [] を返す。
- n が大きく、かつ Python の再帰制限を超えると RecursionError になる可能性がある。
"""

def sieve_recursive(n: int) -> list[int]:
    """エラトステネスの篩（再帰版）で 2〜n の素数リストを返す。"""
    if n < 2:
        return []

    # --- 共通の真偽値リストを用意 ---------------------------------
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False

    import math
    limit = int(math.isqrt(n))

    # --- 内側：p の倍数を順番に消す再帰関数 ------------------------
    def mark_multiples(p: int, k: int) -> None:
        """
        「p の k 倍」を消していき、n を超えたら終了する再帰関数。

        引数:
            p: 今処理している素数（または素数候補）
            k: 何倍目を消すかを表す整数（2, 3, 4, ...）

        処理の流れ:
            1. m = p * k を計算する
            2. もし m > n なら、すべての倍数を処理し終えたので return
            3. m <= n なら、is_prime[m] を False にして「素数ではない」とマーク
            4. k を 1 つ増やして、自分自身を呼び出す（次の倍数を処理）
        """
        m = p * k
        if m > n:
            # 再帰終了条件：n を超えたらおしまい
            return

        # m は p の倍数なので、素数ではない。
        is_prime[m] = False

        # 次の倍数（(k+1)倍）を処理するために、自分自身を呼ぶ。
        mark_multiples(p, k + 1)

    # --- 外側：p を 2,3,4,... と進める再帰関数 ----------------------
    def sieve_from(p: int) -> None:
        """
        p から始めて、limit まで順番に篩にかけていく再帰関数。

        引数:
            p: 現在チェック中の整数（2, 3, 4, ... と増えていく）

        処理の流れ:
            1. もし p*p > n なら、残りはすでに判定済みなので終了（return）
            2. is_prime[p] が True なら、
                - p は素数なので、その倍数を mark_multiples で消す
            3. 次の p（p+1）に進むため、自分自身を呼び出す
        """
        # 再帰終了条件その1：p が √n より大きくなったら終了。
        if p * p > n:
            return

        if is_prime[p]:
            # p が素数のとき、その倍数を再帰で消す
            # 最初は k=2 (p*2) から消していく。
            mark_multiples(p, 2)

        # 次の p に進む（p+1）。
        sieve_from(p + 1)

    # 実際に 2 から篩を開始する。
    sieve_from(2)

    # True のところだけを集めて素数リストにする。
    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return primes


# 非再帰版との比較テスト
if __name__ == "__main__":
    N = 50
    print(f"2〜{N} の素数（非再帰版）:", sieve_iterative(N))
    print(f"2〜{N} の素数（再帰版）  :", sieve_recursive(N))
