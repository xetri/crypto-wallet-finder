package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"runtime"
	"sync"
)

var (
	numThreads = runtime.NumCPU()
	DIFF       = big.NewInt(7)
)

func main() {

	fmt.Println("Scanning:>")

	var wg sync.WaitGroup
	for range numThreads {
		wg.Add(1)
		defer wg.Done()
		go func() {
			for {
				privKeyBytes := make([]byte, 32)
				_, err := rand.Read(privKeyBytes)
				if err != nil {
					panic(err)
				}

				privateKey := new(big.Int).SetBytes(privKeyBytes)

				scanRange(new(big.Int).Sub(privateKey, DIFF), new(big.Int).Add(privateKey, DIFF))
			}
		}()
	}
	wg.Wait()
}

func scanRange(start, end *big.Int) {
	current := new(big.Int).Set(start)
	one := big.NewInt(1)

	for current.Cmp(end) <= 0 {
		privKey := current.Text(16)
		addresses := getAllAddress(current)

		fmt.Printf("PrivateKey: %v\n", privKey)
		for c := range addresses {
			address := addresses[c]
			balance, _ := BitcoinBalance(address)

			if balance > 0 {
				ref := fmt.Sprintf("Found [%v] ! Address: %v =>  Key: %v | Wif: %v\n", balance, address, privKey, PrivateKeyToWIF(current, true))
				fmt.Print(ref)
				saveToFile("satoshis-founds.txt", ref)
			}

			// fmt.Println(address)
		}
		current.Add(current, one)
	}
}

func getAllAddress(privateKey *big.Int) []string {
	addresses := []string{}

	//compressed
	publicKey := PublicKey(privateKey, true)
	addr := []string{
		P2PKH_Address(publicKey),
		P2WPKH_Address(publicKey),
		P2SH_P2WPKH_Address(publicKey),
		P2WSH_P2WPKH_Address(publicKey),
		P2SH_P2PKH_Address(publicKey),
		P2WSH_P2PKH_Address(publicKey),
	}
	addresses = append(addresses, addr...)

	//uncompressed
	publicKey = PublicKey(privateKey, false)
	addr = []string{
		P2PKH_Address(publicKey),
		P2WPKH_Address(publicKey),
		P2SH_P2WPKH_Address(publicKey),
		P2WSH_P2WPKH_Address(publicKey),
		P2SH_P2PKH_Address(publicKey),
		P2WSH_P2PKH_Address(publicKey),
	}
	addresses = append(addresses, addr...)

	return addresses
}

func saveToFile(fpath, data string) {
	f, err := os.OpenFile(fpath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer f.Close() // Ensure file is closed after function returns

	_, err = f.WriteString(data + "\n") // Append key with a newline
	if err != nil {
		fmt.Println("Error appending to file:", err)
	} else {
		fmt.Println("Private key appended to found_key.txt")
	}
}
