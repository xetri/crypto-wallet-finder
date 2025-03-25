package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
)

type BlockchainInfoResponse int

type BlockcypherResponse struct {
    Address             string  `json:"address"`
    TotalReceived       int     `json:"total_received"`
    TotalSent           int     `json:"total_sent"`
    Balance             int     `json:"balance"`
    UnconfirmedBalance  int     `json:"unconfirmed_balance"`
    FinalBalance        int     `json:"final_balance"`
    NTx                 int     `json:"n_tx"`
    UnconfirmedNTx      int     `json:"unconfirmed_n_tx"`
    FinalNTx            int     `json:"final_n_tx"`
}

type ChainflyerResponse struct {
    Address             string  `json:"address"`
    UnconfirmedBalance  int     `json:"unconfirmed_balance"`
    ConfirmedBalance    int     `json:"confirmed_balance"`
}

type BTCScanResponse struct {
    Address             string          `json:"address"`
    ChainStats          BTCScanStats    `json:"chain_stats"`
    MempoolStats        BTCScanStats    `json:"mempool_stats"`
}

type BTCScanStats struct {
    FundedTxoCount      int     `json:"funded_txo_count"`
    FundedTxoSum        int     `json:"funded_txo_sum"`
    SpentTxoCount       int     `json:"spent_txo_count"`
    SpentTxoSum         int     `json:"spent_txo_sum"`
    TxCount             int     `json:"tx_count"`
}


func blockchainInfoBalance(address string) (int, bool) {
    url := "https://blockchain.info/q/addressbalance/" + address
    balance := 0

    resp, err := http.Get(url)
    if err != nil {
        return balance, true
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return balance, true
    }

    var balanceResponse BlockchainInfoResponse
    err = json.Unmarshal(body, &balanceResponse)
    if err != nil {
        return balance, true
    }
    balance = int(balanceResponse)

    return balance, false
}

func blockcypherBalance(address string) (int, bool) {
    url :=  "https://api.blockcypher.com/v1/btc/main/addrs/" + address + "/balance"
    balance := 0

    resp, err1 := http.Get(url)
    if err1 != nil {
        return balance, true
    }
    defer resp.Body.Close()

    body, err2 := ioutil.ReadAll(resp.Body)
    if err2 != nil {
        return balance, true
    }

    var balanceResponse BlockcypherResponse
    err3 := json.Unmarshal(body, &balanceResponse)
    if err3 != nil {
        return balance, true
    }
    balance = balanceResponse.FinalBalance
    
    return balance, false
}

func chainflyerBalance(address string) (int, bool) {
    url := "https://chainflyer.bitflyer.jp/v1/address/" + address
    balance := 0

    resp, err1 := http.Get(url)
    if err1 != nil {
        return balance, true
    }
    defer resp.Body.Close()

    body, err2 := ioutil.ReadAll(resp.Body)
    if err2 != nil {
        return balance, true
    }

    var balanceResponse ChainflyerResponse
    err3 := json.Unmarshal(body, &balanceResponse)
    if err3 != nil {
        return balance, true
    }
    balance = balanceResponse.UnconfirmedBalance + balanceResponse.ConfirmedBalance

    return balance, false
}

func btcscanBalance(address string) (int, bool) {
    url := "https://btcscan.org/api/address/" + address
    balance := 0

    resp, err1 := http.Get(url)
    if err1 != nil {
        return balance, true
    }
    defer resp.Body.Close()

    body, err2 := ioutil.ReadAll(resp.Body)
    if err2 != nil {
        return balance, true
    }

    var balanceResponse BTCScanResponse
    err3 := json.Unmarshal(body, &balanceResponse)
    if err3 != nil {
        return balance, true
    }
    balance = balanceResponse.ChainStats.FundedTxoSum + balanceResponse.ChainStats.SpentTxoSum

    return balance, false
}

var balanceApis = [...] func(string)(int, bool) {
    blockchainInfoBalance,
    blockcypherBalance,
    chainflyerBalance,
    btcscanBalance,
}

func BitcoinBalance(address string) (int, bool) {
    const MAX_TRIAL = 3
    trialOut := 0

    for trialOut < MAX_TRIAL {
        for c := range balanceApis {
            bal, failed := balanceApis[c](address)
            if failed {
                continue
            }
            return bal, false
        }

        trialOut++
    }

    return 0, true
}
