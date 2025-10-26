# This class is used to check if a number is within a given range
class NumberRangeChecker:
    def __init__(self, lower_limit, upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    # This method checks if a given number is within the range of the NumberRangeChecker object
    def is_within_range(self, number) -> bool:
        # Return True if the number is within the range, otherwise return False
        return self.lower_limit <= number <= self.upper_limit