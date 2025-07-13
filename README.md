# 🌾 GramFinance: DeFi for Financial Inclusion

**Built by Team Data Miners**

GramFinance is a decentralized finance (DeFi) platform and AI chatbot designed to bring banking services—such as savings, loans, insurance, and credit scoring—to financially underserved populations in rural India.

## 🚀 Problem We’re Solving

Millions in rural India are excluded from the formal financial system due to:
- Lack of credit history → No loans
- No smartphones → No apps
- Low financial literacy

Yet, most use feature phones, WhatsApp, and UPI. GramFinance bridges this gap.

---

## 💡 Our Solution

GramFinance offers a **WhatsApp-integrated AI Agent** that empowers local financial agents to provide accessible DeFi services:

- 🔐 **Aadhaar + UPI-based Identity Verification**
- 📈 **AI-Powered Credit Scoring** from UPI/bill data
- 🤖 **AI Chatbot in Local Languages** (Hindi, Tamil, Kannada, etc.)
- 🐄 **Micro-Loans (₹500–₹5,000)** via Ethereum smart contracts
- 🧠 **Smart Savings & Insurance Recommendations**
- 🔊 **Voice-Enabled Commands** for low-literacy users

---

## 🧩 System Architecture

### ✅ Frontend
- React.js + Tailwind CSS
- Mobile-first, offline-friendly design
- Wallet integration via MetaMask / WalletConnect

### ✅ Backend
- Node.js + Express.js
- API for agent onboarding, profile management, and data sync

### ✅ Blockchain Layer
- Solidity smart contracts on **Polygon Mumbai Testnet**
- Contracts:
  - `AgentRegistry`: Manages verified agents
  - `LoanContract`: Issues micro-loans
  - `SavingsPool`: Handles user savings
  - `RewardsModule`: Agent incentives

---

## ⚙️ Technologies Used

| Component    | Tech Stack                            |
|--------------|----------------------------------------|
| Frontend     | React.js, Tailwind CSS                 |
| Backend      | Node.js, Express.js                    |
| Blockchain   | Solidity, Hardhat, Polygon             |
| Wallets      | MetaMask, WalletConnect                |
| Storage      | Firebase, IPFS                         |
| Analytics    | Firebase Analytics                     |
| Versioning   | Git, GitHub                            |

---

## 🎯 Key Features

- ✅ **Agent Registration & KYC** via Aadhaar + Polygon ID
- 💸 **DeFi Access** for micro-loans, savings, insurance
- 📊 **On-chain Credit History** for financial reputation
- 🌐 **Low-bandwidth / Offline Agent Support**
- 🎁 **Incentive System** for local agents

---

## 📖 Example Story: Meena's Journey

> Meena, a 32-year-old dairy farmer in Tamil Nadu, uses voice commands in Tamil to apply for a ₹5,000 loan via GramFinance. Within minutes, her Aadhaar is verified, a wallet is created, the loan is disbursed, and she starts repaying monthly. She even buys livestock insurance—all without navigating complex apps.

---

## 🧠 Challenges & Learnings

- Simplifying DeFi UX for low-literacy users
- Building trust in digital agents with local context
- Efficient use of Layer 2 solutions (Polygon) for gas savings

---

## 🔭 Future Scope

- 🇮🇳 eKYC + Aadhaar integration at scale
- 🪙 Tokenomics for agents and users
- 🛡️ Advanced DeFi services: health insurance, mutual funds
- 📲 WhatsApp-first deployments with local language AI

---

## 🛠️ How to Run

```bash
# Install dependencies
npm install

# Start backend
npm run server

# Start frontend
npm run client

# Deploy smart contracts (Hardhat)
npx hardhat deploy
