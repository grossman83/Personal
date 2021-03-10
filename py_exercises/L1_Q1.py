


def factorial(k):
	if k>1:
		return k * factorial(k-1)
	else:
		return 1



if __name__ == '__main__':
	num = 8
	result = factorial(num)
	print(result)


