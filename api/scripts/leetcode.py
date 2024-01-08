# Given
# an
# array
# of
# integers
# nums and an
# integer
# target,
# return indices
# of
# the
# two
# numbers
# such
# that
# they
# add
# up
# to
# target.

# You
# may
# assume
# that
# each
# input
# would
# have
# exactly
# one
# solution, and you
# may
# not use
# the
# same
# element
# twice.
#
# You
# can
# return the
# answer in any
# order.
#
# Example
# 1:
#
# Input: nums = [2, 7, 11, 15], target = 9
# Output: [0, 1]
# Explanation: Because
# nums[0] + nums[1] == 9, we
# return [0, 1].
#
# Example
# 2:
#
# Input: nums = [3, 2, 4], target = 6
# Output: [1, 2]
#
# Example
# 3:
#
# Input: nums = [3, 3], target = 6
# Output: [0, 1]
#
# Constraints:
#
# 2 <= nums.length <= 104
# -109 <= nums[i] <= 109
# -109 <= target <= 109
# Only
# one
# valid
# answer
# exists.
#
# Follow - up: Can
# you
# come
# up
# with an algorithm that is less than O(n2) time complexity?



class Solution(object):
	def twoSum(self, nums, target):
		"""
		:type nums: List[int]
		:type target: int
		:rtype: List[int]
		"""
		return next((i, j) for i, x in enumerate(nums) for j, y in enumerate(nums[ i +1:], i+ 1) if x + y == target)

#
# You
# are
# given
# two
# non - empty
# linked
# lists
# representing
# two
# non - negative
# integers.The
# digits
# are
# stored in reverse
# order, and each
# of
# their
# nodes
# contains
# a
# single
# digit.Add
# the
# two
# numbers and
# return the
# sum as a
# linked
# list.
#
# You
# may
# assume
# the
# two
# numbers
# do
# not contain
# any
# leading
# zero, except the
# number
# 0
# itself.
#
# Example
# 1:
#
# Input: l1 = [2, 4, 3], l2 = [5, 6, 4]
# Output: [7, 0, 8]
# Explanation: 342 + 465 = 807.
#
# Example
# 2:
#
# Input: l1 = [0], l2 = [0]
# Output: [0]
#
# Example
# 3:
#
# Input: l1 = [9, 9, 9, 9, 9, 9, 9], l2 = [9, 9, 9, 9]
# Output: [8, 9, 9, 9, 0, 0, 0, 1]
#
# Constraints:
#
# The
# number
# of
# nodes in each
# linked
# list is in the
# range[1, 100].
# 0 <= Node.val <= 9
# It is guaranteed
# that
# the
# list
# represents
# a
# number
# that
# does
# not have
# leading
# zeros.


class ListNode:
	def __init__(self, val):
		self.val = val
		self.next = None

class Solution:
	def addTwoNumbers(self, l1, l2):
		dummyHead = ListNode(0)
		tail = dummyHead
		carry = 0

		while l1 is not None or l2 is not None or carry != 0:
			digit1 = l1.val if l1 is not None else 0
			digit2 = l2.val if l2 is not None else 0

			sum = digit1 + digit2 + carry
			digit = sum % 10
			carry = sum // 10

			newNode = ListNode(digit)
			tail.next = newNode
			tail = tail.next

			l1 = l1.next if l1 is not None else None
			l2 = l2.next if l2 is not None else None

		result = dummyHead.next
		dummyHead.next = None
		return result


# User
# Given
# a
# string
# s, find
# the
# length
# of
# the
# longest
# substring
# without
# repeating
# characters.
#
# Example
# 1:
#
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The
# answer is "abc",
# with the length of 3.
#
# Example
# 2:
#
# Input: s = "bbbbb"
# Output: 1
# Explanation: The
# answer is "b",
# with the length of 1.
#
# Example
# 3:
#
# Input: s = "pwwkew"
# Output: 3
# Explanation: The
# answer is "wke",
# with the length of 3.
# Notice
# that
# the
# answer
# must
# be
# a
# substring, "pwke" is a
# subsequence and not a
# substring.
#
# Constraints:
#
# 0 <= s.length <= 5 * 104
# s
# consists
# of
# English
# letters, digits, symbols and spaces.


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        start = result = 0
        seen = {}
        for i, letter in enumerate(s):
            if seen.get(letter, -1) >= start:
                start = seen[letter] + 1
            result = max(result, i - start + 1)
            seen[letter] = i
        return result
