package tests

import (
	"bytes"
	"context"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/flow-hydraulics/flow-wallet-api/accounts"
	"github.com/flow-hydraulics/flow-wallet-api/flow_helpers"
	"github.com/flow-hydraulics/flow-wallet-api/handlers"
	"github.com/flow-hydraulics/flow-wallet-api/tests/internal/test"
	"github.com/flow-hydraulics/flow-wallet-api/transactions"
	"github.com/gorilla/mux"
	"github.com/onflow/cadence"
	c_json "github.com/onflow/cadence/encoding/json"
	"github.com/onflow/flow-go-sdk"
)

func TestEmulatorAcceptsSignedTransaction(t *testing.T) {
	cfg := test.LoadConfig(t, testConfigPath)
	svcs := test.GetServices(t, cfg)

	accHandler := handlers.NewAccounts(test.Logger(), svcs.GetAccounts())
	txHandler := handlers.NewTransactions(test.Logger(), svcs.GetTransactions())

	router := mux.NewRouter()
	router.Handle("/", accHandler.Create()).Methods(http.MethodPost)
	router.Handle("/{address}/sign", txHandler.Sign()).Methods(http.MethodPost)

	// Create signing account.
	var account accounts.Account
	res := send(router, http.MethodPost, "/?sync=true", nil)
	assertStatusCode(t, res, http.StatusCreated)
	fromJsonBody(t, res, &account)

	// Transaction:
	code := "transaction(greeting: String) { prepare(signer: AuthAccount){} execute { log(greeting.concat(\", World!\")) }}"
	args := "[{\"type\":\"String\",\"value\":\"Hello\"}]"

	// Sign it.
	body := bytes.NewBufferString(fmt.Sprintf("{\"code\":%q,\"arguments\":%s}", code, args))
	res = send(router, http.MethodPost, fmt.Sprintf("/%s/sign", account.Address), body)
	assertStatusCode(t, res, http.StatusCreated)

	var txResp transactions.SignedTransactionJSONResponse
	fromJsonBody(t, res, &txResp)

	tx := flow.NewTransaction().
		SetScript([]byte(txResp.Code)).
		SetReferenceBlockID(flow.HexToID(txResp.ReferenceBlockID)).
		SetGasLimit(txResp.GasLimit).
		SetProposalKey(flow.HexToAddress(txResp.ProposalKey.Address), txResp.ProposalKey.KeyIndex, txResp.ProposalKey.SequenceNumber).
		SetPayer(flow.HexToAddress(txResp.Payer))

	for _, arg := range txResp.Arguments {
		v, err := asCadence(&arg)
		if err != nil {
			t.Fatal(err)
		}
		tx.AddArgument(v)
	}

	for _, a := range txResp.Authorizers {
		tx.AddAuthorizer(flow.HexToAddress(a))
	}

	for _, s := range txResp.PayloadSignatures {
		bs, err := hex.DecodeString(s.Signature)
		if err != nil {
			t.Fatal(err)
		}
		tx.AddPayloadSignature(flow.HexToAddress(s.Address), s.KeyIndex, bs)
	}

	for _, s := range txResp.EnvelopeSignatures {
		bs, err := hex.DecodeString(s.Signature)
		if err != nil {
			t.Fatal(err)
		}
		tx.AddEnvelopeSignature(flow.HexToAddress(s.Address), s.KeyIndex, bs)
	}

	ctx := context.Background()
	client := test.NewFlowClient(t, cfg)
	_, err := flow_helpers.SendAndWait(ctx, client, *tx, 10*time.Minute)
	if err != nil {
		t.Fatal(err)
	}
}

func assertStatusCode(t *testing.T, res *http.Response, expected int) {
	t.Helper()
	if res.StatusCode != expected {
		bs, err := ioutil.ReadAll(res.Body)
		if err != nil {
			panic(err)
		}
		t.Fatalf("expected HTTP response status code %d, got %d: %s", expected, res.StatusCode, string(bs))
	}
}

func asCadence(a *transactions.CadenceArgument) (cadence.Value, error) {
	c, ok := (*a).(cadence.Value)
	if ok {
		return c, nil
	}

	// Convert to json bytes so we can use cadence's own encoding library
	j, err := json.Marshal(a)
	if err != nil {
		return cadence.Void{}, err
	}

	// Use cadence's own encoding library
	c, err = c_json.Decode(j)
	if err != nil {
		return cadence.Void{}, err
	}

	return c, nil
}

func fromJsonBody(t *testing.T, res *http.Response, v interface{}) {
	t.Helper()

	bs, err := ioutil.ReadAll(res.Body)
	if err != nil {
		t.Fatal(err)
	}

	err = json.Unmarshal(bs, v)
	if err != nil {
		t.Fatal(err)
	}
}

func send(router *mux.Router, method, path string, body io.Reader) *http.Response {
	req := httptest.NewRequest(method, path, body)
	req.Header.Set("content-type", "application/json")
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	return rr.Result()
}
