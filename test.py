from typing import List
def findTheArrayConcVal(nums: List[int]) -> int:
        value = 0
        for i in range(len(nums)//2):
            concatenated_value = str(nums[i]) + str(nums[len(nums)-1-i])
            value += int(concatenated_value)
            print(value)
        return value
    
n = [7,52,4,6]
rst = findTheArrayConcVal(n)
print(rst)