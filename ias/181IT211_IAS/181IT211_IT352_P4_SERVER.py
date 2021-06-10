import socket

def main():
	TC = int(input("Please enter the Test Case number : "))
	op_file = "181IT211_IT352_P4_Output_TC"+str(TC)+"_Serverside.txt"
	op_file = open(op_file, "w")
	S = socket.socket()
	host = socket.gethostname()
	port = 3369
	S.bind((host, port))
	S.listen(5)
	client, addr = S.accept()
	print("Connection from ", addr)
	rnd = 1
	while rnd < 3:
		print("Round : ", rnd)
		op_file.write("\nRound : " + str(rnd) + "\n")
		P = int(input("Enter prime number (P) : "))
		Q = int(input("Enter prime number (Q) : "))
		chlng = int(input("Enter the Challenge (c) : "))
		priv_key = int(input("Enter the Private key (s) : "))
		n = P*Q
		msg = FSP_Server(n, priv_key, chlng, client, op_file, S)
		if msg == "error":
			break
		rnd += 1
	S.close()
	op_file.close()


def FSP_Server(n, priv_key, chlng, client, op_file, S):
	if priv_key < 1 or priv_key > (n-1):
		print("Private key is Invalid")
		op_file.write("Private key Invalid\n")
		print("Connection Terminated")
		op_file.write("Connection Terminated\n")
		S.close()
		client.close()
		return "error"
	else:
		print("Private key (s) : ", priv_key)
		op_file.write("Private key (s) : " + str(priv_key) + "\n")

	pub_key = exp(priv_key, 2, n)
	print("Public key (v) : ", pub_key)
	op_file.write("Public key (v) : " + str(pub_key) + "\n")


	try:
		wtns = client.recv(10000000)
	except socket.timeout:
		print("Connection Timeout")
		return "error"
	wtns = int(wtns.decode("ascii"))
	print("Witness (x) : ", wtns)
	op_file.write("Witness (x) : " + str(wtns) + "\n")

	if chlng !=0 and chlng !=1:
		print("Challenge is Invalid \n")
		op_file.write("Challenge is Invalid ")
		return "error"

	client.send(str(chlng).encode("ascii"))
	print("Challenge (c) : ", chlng)
	op_file.write("Challenge (c) : " + str(chlng) + "\n")

	resp = client.recv(100000)
	resp = int(resp.decode("ascii"))
	print("Response (y) : ", resp)
	op_file.write("Response (y) : " + str(resp) + "\n")

	chk1 = exp(resp, 2, n)
	chk2 = (wtns * exp(pub_key, chlng, n)) % n
	print("(y^2)mod n : {} and x*(v^c)mod n : {}" .format(chk1, chk2))
	op_file.write("(y^2)mod n : {} and x*(v^c)mod n : {}" .format(chk1, chk2))
	if chk1 == chk2:
		print("Yes (It's probable)")
		op_file.write("\nYes (It's probable)")
	else:
		print("No (It's improbable)")
		op_file.write("\nNo (It's improbable)")
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