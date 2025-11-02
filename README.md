# Tetris Game with Flask and User Authentication

Welcome to the **Tetris Game** built in Python! This project combines a classic Tetris game with a full backend using **Flask**, user authentication, and a modern frontend using **Tailwind CSS** via CDN.

---

## 🕹️ Features

- **Classic Tetris Gameplay**  
  Play the classic Tetris game directly in your browser.

- **User Authentication System**  
  - Users can **sign up** with an email, username, and password.  
  - Users can **log in** anytime to access their account.  
  - Passwords are securely stored using hashing.

- **Backend Integration**  
  - Built with **Flask** for routing, authentication, and serving the game.  
  - Connects the frontend and backend seamlessly.  

- **Frontend Design**  
  - Uses **Tailwind CSS via CDN** for styling.  
  - Clean and responsive layout for the game and authentication pages.

---

## ⚡ Technologies Used

- **Python**  
- **Flask**  
- **SQLite** (for storing user accounts)  
- **HTML & Tailwind CSS** (frontend design)  
- **Werkzeug** (password hashing)  

---

## 📦 Installation

1. **Clone the repository**  
```bash
git clone https://github.com/brenoviske/DiceGame.git
cd DiceGame
```
Install your virtual enviroment:
```bash
python3/python -m venv env
source env/bin/activate ( for macOS)
.env\Scripts\activate ( for windows after releasing the exectuion police) 
```

Now installl the dependencies within the virutal enviroment:

```bash
pip install requirements.txt
```

And then run the programm with the main file of the script:
```bash
python3/python app.py
```
