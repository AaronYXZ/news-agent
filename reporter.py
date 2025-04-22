import requests
from openai import OpenAI
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

# Load configuration from YAML
with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

class HotspotReporter:
    def __init__(self):
        self.ds = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=CONFIG['deepseek_api_key'],
        )
        os.makedirs(CONFIG["output_dir"], exist_ok=True)

    def fetch_hotspots(self, source):
        if source == "baidu":
            return self._fetch_baidu_hot()
        elif source == "weibo":
            return self._fetch_weibo_hot()
        return []

    def _fetch_baidu_hot(self):
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "source": "baidu",
                    "title": item.get("word"),
                    "url": item.get("url"),
                    "hot_score": item.get("hotScore")
                }
                for item in data.get("data", {}).get("cards", [{}])[0].get("content", [])
            ][:10]
        except Exception as e:
            print(f"Failed to fetch Baidu trending topics: {e}")
            return []

    def _fetch_weibo_hot(self):
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "source": "weibo",
                    "title": item.get("word"),
                    "url": f"https://s.weibo.com/weibo?q={item.get('word')}",
                    "hot_score": item.get("raw_hot")
                }
                for item in data.get("data", {}).get("realtime", [])
            ][:10]
        except Exception as e:
            print(f"Failed to fetch Weibo trending topics: {e}")
            return []

    def generate_report(self, all_hotspots):
        if not all_hotspots:
            return "No trending data today."
        prompt = self._build_prompt(all_hotspots)
        try:
            response = self.ds.chat.completions.create(
                model="deepseek-v3-250324",
                messages=[
                    {"role": "system", "content": "You are an AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek analysis failed: {e}")
            return "Failed to generate report."

    def _build_prompt(self, hotspots):
        hotspots_str = "\n".join(
            f"{idx + 1}. [{item['source']}] {item['title']} (Hotness: {item.get('hot_score', 'N/A')})"
            for idx, item in enumerate(hotspots)
        )
        return f"""You are a senior industry analyst. Please generate a professional report based on the following trending events:

        Today's trending list:
        {hotspots_str}

        Report requirements:
        1. Select 3-5 most influential events, prioritizing cross-platform topics
        2. Analyze each event in about 200 words, including:
           - Background
           - Possible impacts
           - Reactions from stakeholders
        3. Overall industry trend analysis
        4. Actionable business advice

        Report format:
        # {datetime.now().strftime('%Y-%m-%d')} Hotspot Analysis Report

        ## Key Event Analysis
        ### 1. [Event Title]
        [Analysis]

        ### 2. [Event Title]
        [Analysis]

        ## Trends and Recommendations
        [Your professional insights]
        """

    def save_report(self, report_content):
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{CONFIG['output_dir']}/{today}_hotspot_report.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Report saved to {filename}")

    def send_report(self, report_content):
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"{today} Hotspot Analysis Report"
        msg = MIMEMultipart()
        msg["From"] = CONFIG["email"]["sender"]
        msg["To"] = CONFIG["email"]["receiver"]
        msg["Subject"] = subject
        msg.attach(MIMEText(report_content, "plain"))
        try:
            with smtplib.SMTP_SSL(CONFIG["email"]["smtp_server"], CONFIG["email"].get("smtp_port", 465)) as server:
                server.login(CONFIG["email"]["sender"], CONFIG["email"]["password"])
                server.sendmail(
                    CONFIG["email"]["sender"],
                    CONFIG["email"]["receiver"],
                    msg.as_string()
                )
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
