
def fetch_dict(num):
	the_dict = {}
	for n in range(num)[1:]:
		the_dict[str(n)] = n**2
	return the_dict






if __name__ == '__main__':
	blah = fetch_dict(8)

	print(blah)