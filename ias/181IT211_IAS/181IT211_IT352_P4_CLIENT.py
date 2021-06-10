import socket


def main():
	test_case = int(input("Please enter the Test Case number : "))
	op_file = "181IT211_IT352_P4_Output_TC"+str(test_case)+"_Clientside.txt"
	op_file = open(op_file, "w")
	S = socket.socket()
	host = socket.gethostname()
	port = 3369
	S.connect((host, port))
	rnd = 1
	while rnd<3:
		print("Round : ", rnd)
		op_file.write("\n Round : " + str(rnd) + "\n")
		P = int(input("Enter prime number (P) : "))
		Q = int(input("Enter prime number (Q) : "))
		rand_num = int(input("Enter the Random number (r) : "))
		priv_key = int(input("Enter the Private key (s) : "))
		n = P*Q
		msg = FSP_Client(n, priv_key, rand_num, S, op_file)
		if msg == "error":
			break
		rnd += 1
	S.close()
	op_file.close()


def FSP_Client(n, priv_key, rand_num, S, op_file):
	if priv_key < 1 or priv_key > (n-1):
		print("Private key is Invalid")
		op_file.write("Private key is Invalid \n")
		S.close()
		return "error"
	else:
		print("Private key (s) : ", priv_key)
		op_file.write("Private key (s) : " + str(priv_key) + "\n")
	
	pub_key = exp(priv_key, 2, n)
	print("Public key (v) : ", pub_key)
	op_file.write("Public key (v) : " + str(pub_key) + "\n")

	if rand_num < 1 or rand_num > (n-1):
		print("Random number is Invalid ")
		op_file.write("Random number Invalid  \n")
		print("Connection Terminated")
		op_file.write("Connection Terminated\n")
		S.close()
		return "error"

	print("Random number (r) : ", rand_num)
	op_file.write("Random number (r) : " + str(rand_num) + "\n")

	wtns = exp(rand_num, 2, n)

	S.send(str(wtns).encode("ascii"))
	print("Witness (x) : ", wtns)
	op_file.write("Witness (x) : " + str(wtns) + "\n")

	chlng = S.recv(2048)
	chlng = int(chlng.decode("ascii"))
	print("Challenge (c) : ", chlng)
	op_file.write("Challenge (c) : " + str(chlng) + "\n")

	resp = (rand_num * exp(priv_key, chlng, n)) % n
	S.send(str(resp).encode("ascii"))
	print("Response (y) : ", resp)
	op_file.write("Response (y) : " + str(resp) + "\n")
	return

	
def exp(x, y, n):
	res = 1
	x = x%n
	while y != 0:
		if y & 1:
			res = (res * x)%n
		y = y >> 1
		x = (x * x)%n
	return res

if __name__ == '__main__':
	main()
