from pipelines import run_pipeline

if __name__ == "__main__":
    symbol = "AAPL"   # change to TSLA, INFY, etc.

    result = run_pipeline(symbol)

    print("\n" + "="*60)
    print("📊 FINAL OUTPUT")
    print("="*60)

    print(result["final"])