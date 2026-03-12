# Thorix

[![PyPI](https://img.shields.io/pypi/v/thorix)](https://pypi.org/project/thorix/)
![Main CI](https://github.com/claytonneal/thorix/actions/workflows/on-main.yml/badge.svg)
[![codecov](https://codecov.io/gh/claytonneal/thorix/graph/badge.svg?token=LUD83Q8TB2)](https://codecov.io/gh/claytonneal/thorix)

⚠️ Thorix is currently under development and not ready for production use.

**Thorix** is a modern, Pythonic SDK for interacting with the **VeChain Thor** blockchain.

It provides a clean, strongly-typed interface for reading chain data, building and signing transactions, interacting with smart contracts, and powering analytics, automation, and AI-driven workflows on VeChain.

> **Thorix — Pythonic access to VeChain Thor.**

---

## ✨ Features

- 🐍 **Python-first API** – designed for clarity, type safety, and developer experience  
- 🔐 **Typed domain models** – blocks, transactions, receipts, logs as dataclasses  
- 📦 **Clean layering** – REST JSON → validated schemas → stable domain objects  
- ⚡ **Async & sync clients** – built on `httpx`  
- 🧾 **ABI & contract support** – encode calls, decode events, typed wrappers  
- 🧱 **Multi-clause transactions** – first-class VeChain support  
- ⛽ **Fee delegation aware** – designed with VeChain’s transaction model in mind  
- 📊 **Data-ready** – export chain data to Pandas / Polars for analytics & AI  
- 🤖 **AI-friendly (optional)** – helpers for anomaly detection, clustering, and agents  

---

## 🚀 Installation

Basic install:

```bash
pip install thorix
```
