#This is an implmentation of the BBS PRNG
#Here is a few setup functions to help us out
import random
def gcd(a,b):
    '''
    2.8 times faster than egcd(a,b)[2]
    '''
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

#Cool This one works
#is prime is modified here to also make sure
# That n is congruent to 3mod4
def isprime(n):
    #check if n is prime
    #pick 'a' such that 'a' is an element of {2,..,n-1} 100 times
    # probably too much checking  ¯\_(ツ)_/¯
    for q in range(100):
        a = random.randint(2,n-1)
        if pow(a, n - 1, n) != 1:
            return 0
    # we do not want our prime to be congruent to 1mod4
    if n % 4 == 1:
        return 0
    return 1

#cool this one also works
#Generates a tuple of primes n_bits long
#The primes are n_bits long as well as congruent
# to 3mod4 isn't that neat
def generate_primes(n_bits):
    padder = 1 << n_bits - 1

    p = random.getrandbits(n_bits)

    # p might not have n bits so we just want to make sure the most signigicant bit is a 1
    # bit-wiseOR p with (1 << n_bits - 1)
    # bit-wiseOR p with 1 to ensure oddness 
    p = p | padder
    p = p | 1

    #keep generating primes until we win
    while not isprime(p):
        p = random.getrandbits(n_bits)
        # p might not have n bits so we just want to make sure the most signigicant bit is a 1
        # bit-wiseOR p with (1 << n_bits - 1)
        # bit-wiseOR p with 1
        p = p | padder
        p = p | 1

    q = random.getrandbits(n_bits)

    # p might not have n bits so we just want to make sure the most signigicant bit is a 1
    # bit-wiseOR p with (1 << n_bits - 1)
    # bit-wiseOR p with 1
    q = q | padder
    q = q | 1

    #keep generating primes until we win
    while not isprime(q):
        q = random.getrandbits(n_bits)
        # p might not have n bits so we just want to make sure the most signigicant bit is a 1
        # bit-wiseOR p with (1 << n_bits - 1)
        # bit-wiseOR p with 1
        q = q | padder
        q = q | 1
    return (p, q)

#Okay let us start generating random numbers
#the primes are n_bits long while the output is 
#l bits long
def generate_random_bits(n_bits, l):
    primes = generate_primes(n_bits)
    n = primes[0]*primes[1]
    #generate our seed
    seed = random.randint(1, n-1)
    #make the seed odd
    seed = seed | 1
    while gcd(n, seed) != 1:
        seed = random.randint(1, n-1)
    #we have our seed and our n and our p and q
    z = 0
    x = []
    x.append(pow(seed, 2, n))
    i = 1
    #grab the LSB of x and append it to z
    z = z | (x[0] & 1)
    while i <= l:

        #bit shift r by 1 to the left
        z = z << 1
        #Generate the next x
        x.append(pow(x[i-1], 2, n))
        z = z | (x[i] & 1)
        i += 1
    return z