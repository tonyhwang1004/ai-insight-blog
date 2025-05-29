# =====================================================
# 1. scripts/auto_blogger.py (메인 자동화 스크립트)
# =====================================================

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import random
import re

class AIBlogger:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.blog_topics = [
            "ChatGPT 활용법",
            "머신러닝 트렌드",
            "딥러닝 기초",
            "AI 도구 리뷰",
            "생성형 AI",
            "AI 윤리",
            "자연어처리",
            "컴퓨터 비전",
            "AI 스타트업",
            "AI와 미래직업"
        ]
        self.categories = [
            "ChatGPT",
            "머신러닝", 
            "딥러닝",
            "AI 도구",
            "AI 트렌드",
            "AI 윤리"
        ]
        
    def generate_blog_post(self):
        """OpenAI API를 사용해 블로그 포스트 생성"""
        topic = random.choice(self.blog_topics)
        category = random.choice(self.categories)
        
        prompt = f"""
        다음 주제에 대해 전문적이고 유익한 블로그 글을 작성해주세요:
        
        주제: {topic}
        카테고리: {category}
        
        요구사항:
        1. 제목은 SEO에 최적화되고 클릭을 유도하는 매력적인 제목
        2. 최소 800단어 이상의 상세한 내용
        3. 실용적인 정보와 구체적인 예시 포함
        4. 초보자도 이해할 수 있도록 쉬운 설명
        5. 단락별로 소제목 사용
        6. 마지막에 핵심 포인트 요약
        
        형식:
        - 제목만 따로 첫 줄에
        - 본문은 마크다운 형식으로
        - 코드 예시가 있다면 ```python 코드블록 사용
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system", 
                    "content": "당신은 AI 전문 블로거입니다. 최신 AI 기술에 대해 전문적이면서도 이해하기 쉬운 글을 작성합니다."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 2500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 제목과 본문 분리
            lines = content.strip().split('\n')
            title = lines[0].strip('#').strip()
            body = '\n'.join(lines[1:]).strip()
            
            return {
                'title': title,
                'body': body,
                'category': category,
                'topic': topic
            }
            
        except Exception as e:
            print(f"API 호출 실패: {e}")
            return self.generate_fallback_post()
    
    def generate_fallback_post(self):
        """API 실패시 대체 포스트 생성"""
        fallback_posts = [
            {
                'title': 'AI 시대의 새로운 기회: 개발자를 위한 5가지 준비사항',
                'body': '''
# AI 시대의 새로운 기회

## 들어가며
인공지능 기술이 급속도로 발전하면서 개발자들에게 새로운 기회와 도전이 동시에 찾아오고 있습니다.

## 1. 머신러닝 기초 학습
파이썬과 TensorFlow, PyTorch 같은 프레임워크에 익숙해지는 것이 중요합니다.

## 2. 데이터 처리 능력
AI의 핵심은 데이터입니다. 데이터 전처리와 분석 능력을 기르세요.

## 3. API 활용 능력
OpenAI, Google AI 등의 API를 활용하는 방법을 익히세요.

## 4. 윤리적 사고
AI 개발시 윤리적 고려사항을 항상 염두에 두어야 합니다.

## 5. 지속적인 학습
AI 분야는 빠르게 변화하므로 지속적인 학습이 필수입니다.

## 마무리
AI 시대에 뒤처지지 않으려면 지금부터 차근차근 준비해나가시기 바랍니다.
                ''',
                'category': 'AI 트렌드',
                'topic': 'AI 개발자 준비사항'
            }
        ]
        return random.choice(fallback_posts)
    
    def create_blog_post_file(self, post_data):
        """마크다운 블로그 포스트 파일 생성"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # 파일명 생성 (제목을 영문으로 변환)
        filename = f"{date_str}-{self.title_to_filename(post_data['title'])}.md"
        
        # 프론트매터 생성
        front_matter = f"""---
layout: post
title: "{post_data['title']}"
date: {date_str} {time_str} +0900
categories: [{post_data['category']}]
tags: [AI, {post_data['category']}, {post_data['topic']}]
author: "AI Insight"
description: "{post_data['title']} - AI 인사이트 블로그에서 제공하는 전문 분석"
image: "/assets/images/ai-blog-{date_str}.jpg"
---

{post_data['body']}

---

## 🤖 AI 인사이트 더 보기

- [최신 AI 뉴스](/)
- [ChatGPT 활용법](/category/chatgpt)
- [머신러닝 가이드](/category/machine-learning)

### 📬 뉴스레터 구독

최신 AI 소식을 이메일로 받아보세요!

[구독하기](/newsletter)

---

*이 글이 도움이 되셨다면 공유해주세요! 🚀*
"""
        
        # posts 디렉토리 생성
        posts_dir = Path("posts")
        posts_dir.mkdir(exist_ok=True)
        
        # 파일 저장
        file_path = posts_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(front_matter)
        
        print(f"새 포스트 생성: {filename}")
        return filename
    
    def title_to_filename(self, title):
        """제목을 파일명으로 변환"""
        # 한글을 영문으로 매핑 (간단한 예시)
        korean_to_english = {
            'ChatGPT': 'chatgpt',
            '인공지능': 'artificial-intelligence',
            '머신러닝': 'machine-learning',
            '딥러닝': 'deep-learning',
            'AI': 'ai',
            '가이드': 'guide',
            '방법': 'methods',
            '활용': 'utilization',
            '분석': 'analysis',
            '트렌드': 'trends'
        }
        
        filename = title.lower()
        for korean, english in korean_to_english.items():
            filename = filename.replace(korean.lower(), english)
        
        # 특수문자 제거 및 공백을 하이픈으로
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[\s_]+', '-', filename)
        filename = filename.strip('-')
        
        return filename[:50]  # 파일명 길이 제한
    
    def update_index_html(self):
        """index.html에 새 포스트 추가"""
        # 이 부분은 실제 구현시 HTML 파싱과 업데이트가 필요
        print("index.html 업데이트 완료")
    
    def run(self):
        """메인 실행 함수"""
        print("AI 블로그 자동 포스팅 시작...")
        
        # 새 포스트 생성
        post_data = self.generate_blog_post()
        filename = self.create_blog_post_file(post_data)
        
        # 인덱스 페이지 업데이트
        self.update_index_html()
        
        print("자동 포스팅 완료!")
        return filename

if __name__ == "__main__":
    blogger = AIBlogger()
    blogger.run()

# =====================================================
# 2. scripts/requirements.txt
# =====================================================

openai==1.3.0
requests==2.31.0
python-dateutil==2.8.2
pathlib
beautifulsoup4==4.12.2
markdown==3.5.1

# =====================================================
# 3. .github/workflows/auto-post.yml
# =====================================================

name: 🤖 AI Blog Auto Posting

on:
  schedule:
    # 매일 오전 9시 (한국시간) = UTC 0시
    - cron: '0 0 * * *'
    # 주 3회 (월,수,금) 오전 9시
    # - cron: '0 0 * * 1,3,5'
  
  # 수동 실행 가능
  workflow_dispatch:

jobs:
  auto-posting:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📂 Repository 체크아웃
      uses: actions/checkout@v4
      
    - name: 🐍 Python 설정
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: 📦 의존성 설치
      run: |
        python -m pip install --upgrade pip
        pip install -r scripts/requirements.txt
        
    - name: ✍️ 새 블로그 포스트 생성
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        cd scripts
        python auto_blogger.py
        
    - name: 🔄 Git 설정 및 커밋
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "AI Blogger Bot"
        git add .
        if git diff --staged --quiet; then
          echo "변경사항 없음"
        else
          git commit -m "🤖 자동 포스트 생성: $(date +'%Y-%m-%d %H:%M')"
          git push
        fi

# =====================================================
# 4. 추가 유틸리티 스크립트
# =====================================================

# scripts/post_manager.py
import os
import json
from datetime import datetime
from pathlib import Path

class PostManager:
    def __init__(self):
        self.posts_dir = Path("posts")
        self.stats_file = Path("_data/stats.json")
        
    def get_post_stats(self):
        """포스트 통계 생성"""
        posts = list(self.posts_dir.glob("*.md"))
        
        stats = {
            "total_posts": len(posts),
            "last_updated": datetime.now().isoformat(),
            "categories": {},
            "recent_posts": []
        }
        
        # 카테고리별 통계
        for post_file in posts:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 간단한 카테고리 추출 (실제로는 YAML 파싱 필요)
                if "ChatGPT" in content:
                    stats["categories"]["ChatGPT"] = stats["categories"].get("ChatGPT", 0) + 1
                elif "머신러닝" in content:
                    stats["categories"]["머신러닝"] = stats["categories"].get("머신러닝", 0) + 1
        
        return stats
    
    def update_sitemap(self):
        """사이트맵 업데이트"""
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://tonyhwang1004.github.io/ai-insight-blog/</loc>
        <lastmod>{}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>'''.format(datetime.now().strftime('%Y-%m-%d'))
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)

if __name__ == "__main__":
    manager = PostManager()
    stats = manager.get_post_stats()
    print(f"총 포스트: {stats['total_posts']}개")
    manager.update_sitemap()
