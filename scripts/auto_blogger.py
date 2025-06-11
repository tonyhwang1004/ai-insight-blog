    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 인사이트 블로그 자동 포스팅 시스템
Author: AI Insight Blog Team
Created: 2025-06-11
"""

import sys
import os
import subprocess
import json
import random
from datetime import datetime
from pathlib import Path

def check_and_install_requirements():
    """필요한 라이브러리들을 확인하고 설치"""
    required_packages = ['openai', 'requests', 'beautifulsoup4']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 이미 설치됨")
        except ImportError:
            print(f"📦 {package} 설치 중...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} 설치 완료")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} 설치 실패: {e}")
                return False
    return True

def load_api_key():
    """API 키를 환경변수 또는 .env 파일에서 로드"""
    # 환경변수에서 먼저 확인
    api_key = os.getenv('OPENAI_API_KEY')
    
    # .env 파일에서 확인
    if not api_key and os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"\'')
                        break
        except Exception as e:
            print(f"⚠️ .env 파일 읽기 실패: {e}")
    
    return api_key

def get_ai_topics():
    """AI 관련 블로그 주제 목록 반환"""
    topics = [
        {
            "title": "ChatGPT 최신 업데이트와 새로운 기능들",
            "category": "ChatGPT",
            "keywords": ["ChatGPT", "OpenAI", "AI챗봇", "언어모델"]
        },
        {
            "title": "AI 코딩 어시스턴트 완벽 비교 가이드",
            "category": "AI 도구",
            "keywords": ["GitHub Copilot", "Cursor", "AI코딩", "개발도구"]
        },
        {
            "title": "생성형 AI로 창작하는 새로운 방법들",
            "category": "생성형 AI",
            "keywords": ["이미지생성", "텍스트생성", "창작AI", "Midjourney"]
        },
        {
            "title": "머신러닝 초보자를 위한 실전 가이드",
            "category": "머신러닝",
            "keywords": ["머신러닝", "Python", "데이터사이언스", "알고리즘"]
        },
        {
            "title": "AI 윤리와 책임감 있는 AI 개발",
            "category": "AI 윤리",
            "keywords": ["AI윤리", "편향성", "투명성", "AI규제"]
        },
        {
            "title": "2025년 AI 스타트업 투자 트렌드 분석",
            "category": "AI 트렌드",
            "keywords": ["AI투자", "스타트업", "벤처캐피털", "AI시장"]
        },
        {
            "title": "자연어 처리 기술의 최신 동향",
            "category": "딥러닝",
            "keywords": ["NLP", "Transformer", "BERT", "GPT"]
        },
        {
            "title": "AI를 활용한 비즈니스 자동화 사례들",
            "category": "AI 활용",
            "keywords": ["업무자동화", "RPA", "AI비즈니스", "효율성"]
        }
    ]
    return topics

def generate_blog_post(client, topic_data):
    """GPT를 사용해 블로그 포스트 생성"""
    try:
        prompt = f"""
다음 주제로 한국어 블로그 포스트를 작성해주세요:

주제: {topic_data['title']}
카테고리: {topic_data['category']}
키워드: {', '.join(topic_data['keywords'])}

요구사항:
1. 2000자 이상의 상세하고 전문적인 내용
2. SEO에 최적화된 구조 (제목, 소제목, 목록 등 활용)
3. 실용적인 팁과 예시 포함
4. 독자에게 유용한 정보 제공
5. 자연스럽고 읽기 쉬운 문체

형식:
- 매력적인 제목
- 간단한 도입부
- 3-5개의 주요 섹션 (각각 소제목 포함)
- 실용적인 예시나 팁
- 마무리 및 요약

한국 독자들이 관심 가질만한 최신 정보와 트렌드를 포함해서 작성해주세요.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 AI 전문 블로거입니다. 한국어로 전문적이고 흥미로운 블로그 포스트를 작성하는 전문가입니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ 블로그 포스트 생성 실패: {str(e)}")
        return None

def save_blog_post(title, content, category):
    """생성된 블로그 포스트를 파일로 저장"""
    try:
        # posts 디렉토리 생성
        posts_dir = Path("posts")
        posts_dir.mkdir(exist_ok=True)
        
        # 파일명 생성 (현재 시간 기준)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # 파일명 길이 제한
        filename = f"{timestamp}_{safe_title}.md"
        
        filepath = posts_dir / filename
        
        # 메타데이터와 함께 저장
        post_content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
category: "{category}"
tags: ["AI", "인공지능", "{category}"]
author: "AI Insight Blog"
---

{content}

---

> 이 글이 도움이 되셨다면 공유해주세요! 
> 더 많은 AI 관련 소식은 [AI 인사이트 블로그](https://tonyhwang1004.github.io/ai-insight-blog)에서 확인하세요.
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(post_content)
        
        print(f"✅ 블로그 포스트 저장 완료: {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"❌ 파일 저장 실패: {str(e)}")
        return None

def update_html_with_new_post(title, excerpt, category):
    """HTML 파일에 새 포스트 추가"""
    try:
        # 현재 날짜
        current_date = datetime.now().strftime("%Y.%m.%d")
        view_count = random.randint(50, 500)  # 랜덤 조회수
        
        # 새 포스트 HTML
        new_post_html = f'''                <article class="post-card">
                    <div class="post-meta">
                        <span class="post-category">{category}</span>
                        <span>📅 {current_date}</span>
                        <span>👀 {view_count} views</span>
                    </div>
                    <h2 class="post-title">{title}</h2>
                    <p class="post-excerpt">{excerpt}</p>
                    <a href="#" class="read-more">더 읽기 →</a>
                </article>

'''
        
        # index.html 파일 확인 및 업데이트
        html_file = Path("index.html")
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 첫 번째 post-card 앞에 새 포스트 삽입
            insert_marker = '<main class="blog-posts" id="posts">'
            insert_position = html_content.find(insert_marker)
            
            if insert_position != -1:
                # marker 뒤의 첫 번째 article 찾기
                marker_end = insert_position + len(insert_marker)
                article_start = html_content.find('<article class="post-card">', marker_end)
                
                if article_start != -1:
                    updated_html = (
                        html_content[:article_start] + 
                        new_post_html + 
                        html_content[article_start:]
                    )
                    
                    # 파일 저장
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(updated_html)
                    
                    print("✅ index.html 파일이 업데이트되었습니다.")
                    return True
                else:
                    print("⚠️ HTML 파일에서 기존 post-card를 찾을 수 없습니다.")
            else:
                print("⚠️ HTML 파일에서 blog-posts 섹션을 찾을 수 없습니다.")
        else:
            print("⚠️ index.html 파일을 찾을 수 없습니다.")
            
        return False
        
    except Exception as e:
        print(f"⚠️ HTML 업데이트 중 오류: {str(e)}")
        return False

def log_activity(message):
    """활동 로그 기록"""
    try:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        log_file = logs_dir / "auto_blogger.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
            
    except Exception as e:
        print(f"⚠️ 로그 기록 실패: {str(e)}")

def main():
    """메인 실행 함수"""
    print("🤖 AI 인사이트 블로그 자동 포스팅 시스템 시작")
    log_activity("자동 포스팅 시스템 시작")
    
    # 의존성 확인 및 설치
    print("📦 의존성 확인 중...")
    if not check_and_install_requirements():
        print("❌ 필요한 라이브러리 설치에 실패했습니다.")
        log_activity("의존성 설치 실패")
        sys.exit(1)
    
    # 라이브러리 import
    try:
        from openai import OpenAI
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        print(f"❌ 라이브러리 import 실패: {e}")
        log_activity(f"라이브러리 import 실패: {e}")
        sys.exit(1)
    
    # API 키 확인
    print("🔑 API 키 확인 중...")
    api_key = load_api_key()
    if not api_key:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        print("다음 중 하나의 방법으로 설정하세요:")
        print("1. export OPENAI_API_KEY='your-api-key-here'")
        print("2. .env 파일에 OPENAI_API_KEY=your-api-key-here 추가")
        log_activity("API 키 설정되지 않음")
        sys.exit(1)
    
    try:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI 클라이언트 초기화 완료")
        
        # 주제 선택
        topics = get_ai_topics()
        selected_topic = random.choice(topics)
        
        print(f"📝 선택된 주제: {selected_topic['title']}")
        print(f"📂 카테고리: {selected_topic['category']}")
        log_activity(f"주제 선택: {selected_topic['title']}")
        
        # 블로그 포스트 생성
        print("🤖 AI를 사용해 블로그 포스트 생성 중...")
        blog_content = generate_blog_post(client, selected_topic)
        
        if not blog_content:
            print("❌ 블로그 포스트 생성에 실패했습니다.")
            log_activity("블로그 포스트 생성 실패")
            sys.exit(1)
        
        print("✅ 블로그 포스트 생성 완료")
        
        # 파일 저장
        print("💾 파일 저장 중...")
        saved_file = save_blog_post(
            selected_topic['title'], 
            blog_content, 
            selected_topic['category']
        )
        
        if saved_file:
            log_activity(f"블로그 포스트 저장: {saved_file}")
        
        # HTML 업데이트
        print("🔄 웹사이트 업데이트 중...")
        excerpt = blog_content[:200].replace('\n', ' ').strip() + "..."
        html_updated = update_html_with_new_post(
            selected_topic['title'], 
            excerpt, 
            selected_topic['category']
        )
        
        if html_updated:
            log_activity("HTML 파일 업데이트 성공")
        
        print("🎉 자동 포스팅 완료!")
        print(f"📄 생성된 포스트: {selected_topic['title']}")
        log_activity("자동 포스팅 완료")
        
    except Exception as e:
        error_msg = f"오류 발생: {str(e)}"
        print(f"❌ {error_msg}")
        log_activity(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
