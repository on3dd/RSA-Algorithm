# coding: utf8

'''
620031587
Net-Centric Computing Assignment
Part A - RSA Encryption
'''

import random
import math
import timeit
from Crypto.Util import number

n_length = 2048

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
		while b != 0:
				a, b = b, a % b
		return a

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
		d = 0
		x1 = 0
		x2 = 1
		y1 = 1
		temp_phi = phi
		
		while e > 0:
				temp1 = math.floor(temp_phi/e)
				temp2 = temp_phi - temp1 * e
				temp_phi = e
				e = temp2
				
				x = x2- temp1* x1
				y = d - temp1 * y1
				
				x2 = x1
				x1 = x
				d = y1
				y1 = y
		
		if temp_phi == 1:
				return d + phi
		else:
				return d+phi

'''
Tests to see if a number is prime.
'''

def generate_keypair(p, q):
		if p == q:
				raise ValueError('p and q cannot be equal')
		#n = pq
		n = p * q

		#Phi is the totient of n
		phi = (p-1) * (q-1)

		#Choose an integer e such that e and phi(n) are coprime
		e = random.randrange(1, phi)

		#Use Euclid's Algorithm to verify that e and phi(n) are comprime
		g = gcd(e, phi)
		while g != 1:
				e = random.randrange(1, phi)
				g = gcd(e, phi)

		#Use Extended Euclid's Algorithm to generate the private key
		d = multiplicative_inverse(e, phi)
		
		#Return public and private keypair
		#Public key is (e, n) and private key is (d, n)
		return ((e, n), (d, n))

def compute_mod(a,b,m):
		base = a % m
		result = 1
		while(b>0):
				if(b%2==1):
						result=result*base % m
				b = math.floor(b//2)
				base = base*base %m
		return result

def encrypt(pk, plaintext):
		#Unpack the key into it's components
		key, n = pk
		#Convert each letter in the plaintext to numbers based on the character using a^b mod m
		cipher = [compute_mod(ord(char),key,n) for char in plaintext]
		#Return the array of bytes
		return cipher

def decrypt(pk, ciphertext):
		#Unpack the key into its components
		key, n = pk
		#Generate the plaintext based on the ciphertext and key using a^b mod m
		plain = [chr(compute_mod(char,key,n)) for char in ciphertext]
		#Return the array of bytes as a string
		return ''.join(plain)
		

print("RSA Encrypter/ Decrypter")

p = number.getPrime(n_length)
print("First prime number:", p, '\n')

q = number.getPrime(n_length)
print("Second prime number:", q ,'\n')

print("Generating your public/private keypairs now . . .")
public, private = generate_keypair(p, q)
# print ("Your public key is ", public ," and your private key is ", private)

message = open('input.txt', 'r').read()
encrypted_msg = encrypt(private, message)

# print("Your encrypted message is: ")
# print(''.join(map(lambda x: str(x), encrypted_msg)))

print("Decrypting message with public key . . .")
print("Your message is:")

print(decrypt(public, encrypted_msg))
print('Total time to decrypt:', timeit.timeit("decrypt(public, encrypted_msg)", setup="from __main__ import decrypt, public, encrypted_msg", number=1))
