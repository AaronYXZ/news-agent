
# 🔥 Hotspot Analysis Automation

This system collects trending topics from Baidu and Weibo, generates professional analysis reports using DeepSeek API, and optionally sends them via email. It’s designed to run automatically twice a day and save reports locally.

---

## 🚀 Features

- 📊 **Multi-source hot topic collection** (Baidu & Weibo)
- 🧠 **AI-powered report generation** using DeepSeek
- 💌 **Automated email dispatch** (configurable)
- 🗂️ **Local knowledge base** of daily reports
- ⏱️ **Fully scheduled execution** (10:00 AM & 4:00 PM)

---

## 📦 Installation & Environment Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/AaronYXZ/news-agent
   cd your-repo-folder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `config.yaml`**
   Add your credentials and config:

   ```yaml
   deepseek_api_key: "your-deepseek-api-key"

   email:
     sender: "your_email@example.com"
     receiver: "recipient@example.com"
     password: "your_email_password"
     smtp_server: "smtp.qq.com"
     smtp_port: 465

   data_sources:
     - baidu
     - weibo

   output_dir: "reports"
   ```

---

## 🛠️ Usage

Run the scheduler script:

```bash
python scheduler.py
```

The system will:
- Collect top 10 hot topics from each platform.
- Sort and analyze them using DeepSeek.
- Save the markdown report in the `reports` folder.
- Optionally email the report to the configured recipient.

---

## 🎁 Benefits Observed

- ⏳ **Time Saved**: At least 2 hours saved daily from manual news gathering and summary writing.
- 📈 **Better Insights**: AI-generated content often highlights connections I might miss.
- 📚 **Knowledge Base**: All reports are saved locally for future reference and research.
- ⚡ **Faster Reaction**: I get instant briefings when trends emerge, avoiding missed opportunities.

---

## 🚧 Future Improvements

- Add Slack or Telegram notifications
- Deploy on a cloud function (e.g., AWS Lambda + Scheduler)
- Integrate with internal dashboards (e.g., Notion, Confluence)
- Customize report length and style based on audience

