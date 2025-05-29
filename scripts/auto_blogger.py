#!/usr/bin/env python3
"""
🧪 간단한 테스트 블로거 (OpenAI API 없이 작동)
시스템 동작 확인용
"""

import os
import random
from datetime import datetime
import subprocess
import sys

class SimpleBlogger:
    def __init__(self):
        """초기화"""
        self.posts_dir = "_posts"
        self.ensure_posts_directory()
        
        # 미리 준비된 블로그 포스트 템플릿
        self.blog_templates = [
            {
                'title': 'AI 시대의 새로운 기회: 개발자를 위한 5가지 준비사항',
                'content': '''# AI 시대의 새로운 기회

## 🚀 들어가며
인공지능 기술이 급속도로 발전하면서 개발자들에게 새로운 기회와 도전이 동시에 찾아오고 있습니다. 이 글에서는 AI 시대에 뒤처지지 않기 위해 개발자가 준비해야 할 5가지 핵심 사항을 살펴보겠습니다.

## 1. 머신러닝 기초 학습 🤖
AI 개발의 첫걸음은 머신러닝 기초를 이해하는 것입니다.

### 핵심 기술 스택
- **Python**: 가장 널리 사용되는 AI 개발 언어
- **TensorFlow/PyTorch**: 딥러닝 프레임워크
- **Scikit-learn**: 전통적인 머신러닝 라이브러리
- **Pandas/NumPy**: 데이터 처리 도구

### 학습 로드맵
1. Python 기초 문법 익히기
2. 통계학과 선형대수 기본 개념 학습
3. 머신러닝 알고리즘 이해
4. 실습 프로젝트 진행

## 2. 데이터 처리 능력 향상 📊
AI의 핵심은 데이터입니다. 좋은 데이터 없이는 좋은 AI 모델을 만들 수 없습니다.

### 데이터 처리 스킬
- 데이터 수집과 정제
- 탐색적 데이터 분석 (EDA)
- 특성 엔지니어링
- 데이터 시각화

### 실무 팁
```python
import pandas as pd
import numpy as np

# 데이터 로드 및 기본 정보 확인
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())
```

## 3. API 활용 능력 📡
최신 AI 서비스들은 대부분 API 형태로 제공됩니다.

### 주요 AI API 서비스
- **OpenAI API**: GPT 모델 활용
- **Google Cloud AI**: 다양한 AI 서비스
- **AWS AI Services**: 클라우드 기반 AI 도구
- **Azure Cognitive Services**: 마이크로소프트 AI 플랫폼

### API 활용 예시
```python
import requests

# OpenAI API 예시 (실제 사용시 API 키 필요)
response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers={'Authorization': 'Bearer YOUR_API_KEY'},
    json={
        'model': 'gpt-4',
        'messages': [{'role': 'user', 'content': 'Hello, AI!'}]
    }
)
```

## 4. 윤리적 AI 개발 🔍
AI 기술이 발전할수록 윤리적 고려사항이 중요해집니다.

### 고려사항
- **편향성 제거**: 공정한 AI 모델 개발
- **개인정보 보호**: 데이터 프라이버시 준수
- **투명성**: 설명 가능한 AI 구현
- **책임감**: AI 결과에 대한 책임 의식

### 실무 적용
- 다양한 데이터셋으로 모델 검증
- 정기적인 모델 성능 모니터링
- 사용자 피드백 반영 시스템 구축

## 5. 지속적인 학습과 네트워킹 🌐
AI 분야는 빠르게 변화하므로 지속적인 학습이 필수입니다.

### 학습 리소스
- **온라인 강의**: Coursera, edX, Udacity
- **기술 블로그**: Medium, Towards Data Science
- **연구 논문**: arXiv, Google Scholar
- **커뮤니티**: Reddit, Stack Overflow, 한국 AI 개발자 모임

### 네트워킹 활동
- AI 컨퍼런스 참석
- 오픈소스 프로젝트 기여
- 기술 블로그 작성
- 스터디 그룹 참여

## 마무리 💡
AI 시대는 이미 시작되었고, 준비된 개발자에게는 무한한 기회가 있습니다. 위에서 제시한 5가지 준비사항을 차근차근 실행해나가면, AI 분야에서 성공적인 커리어를 쌓을 수 있을 것입니다.

### 다음 단계
1. 개인 프로젝트로 포트폴리오 구축
2. AI 관련 자격증 취득 고려
3. 실무 경험 쌓기
4. 전문 분야 선택 (NLP, Computer Vision, 추천 시스템 등)

AI 시대의 파도를 타기 위해 지금부터 준비를 시작하세요! 🚀''',
                'category': 'AI General',
                'topic': 'AI 개발자 준비사항'
            },
            {
                'title': 'ChatGPT 프롬프트 엔지니어링: 효과적인 질문 작성법',
                'content': '''# ChatGPT 프롬프트 엔지니어링

## 🎯 프롬프트 엔지니어링이란?
프롬프트 엔지니어링은 AI 모델에게 더 정확하고 유용한 답변을 얻기 위해 질문을 체계적으로 설계하는 기술입니다.

## 핵심 원칙들

### 1. 명확하고 구체적으로 질문하기
- 모호한 질문보다는 구체적인 요구사항 제시
- 원하는 답변의 형태와 길이 명시

### 2. 컨텍스트 제공하기
- 배경 정보와 상황 설명
- 목적과 대상 독자 명시

### 3. 단계별 접근법 활용
- 복잡한 문제는 작은 단위로 분해
- 체계적인 사고 과정 요청

## 실용적인 프롬프트 템플릿

### 기본 구조
```
역할: [AI에게 부여할 역할]
맥락: [상황과 배경 정보]
작업: [구체적인 요청사항]
형식: [원하는 답변 형태]
제약: [지켜야 할 조건들]
```

### 예시 활용
이러한 프롬프트 기법들을 활용하면 ChatGPT로부터 더욱 정확하고 유용한 답변을 얻을 수 있습니다.

## 마무리
프롬프트 엔지니어링은 AI 시대의 필수 스킬입니다. 지속적인 연습을 통해 더 나은 결과를 얻어보세요!''',
                'category': 'ChatGPT',
                'topic': '프롬프트 엔지니어링'
            }
        ]

    def ensure_posts_directory(self):
        """포스트 디렉토리 확인 및 생성"""
        if not os.path.exists(self.posts_dir):
            os.makedirs(self.posts_dir)
            print(f"✅ {self.posts_dir} 디렉토리를 생성했습니다.")

    def generate_blog_post(self):
        """미리 준비된 블로그 포스트 선택"""
        post_data = random.choice(self.blog_templates)
        print(f"🤖 주제: {post_data['topic']}")
        print(f"📂 카테고리: {post_data['category']}")
        return post_data

    def create_post_file(self, post_data):
        """Jekyll 형식의 마크다운 파일 생성"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # 파일명 생성
        safe_title = self.make_safe_filename(post_data['title'])
        filename = f"{date_str}-{safe_title}.md"
        filepath = os.path.join(self.posts_dir, filename)
        
        # Jekyll Front Matter 생성
        front_matter = f"""---
layout: post
title: "{post_data['title']}"
date: {date_str} {time_str} +0900
categories: [{post_data['category']}]
tags: [AI, {post_data['topic']}, 인공지능, 기술]
author: "AI Insight Blog"
description: "{post_data['title']} - 실용적인 AI 가이드와 최신 트렌드 소개"
---

"""
        
        # 전체 콘텐츠 결합
        full_content = front_matter + post_data['content']
        
        # 파일 저장
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"✅ 포스트 파일 생성: {filename}")
            return filepath
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")
            return None

    def make_safe_filename(self, title):
        """파일명으로 사용 가능한 안전한 문자열 생성"""
        import re
        # 한글과 특수문자 제거
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[\s_]+', '-', safe_title)
        safe_title = safe_title.strip('-')
        return safe_title[:50] if len(safe_title) > 50 else safe_title or "ai-blog-post"

    def git_commit_and_push(self, filepath):
        """Git 커밋 및 푸시"""
        try:
            # Git 설정
            subprocess.run(['git', 'config', '--global', 'user.name', 'AI Blogger Bot'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'ai-blogger@github-actions.com'], check=True)
            
            # 파일 추가
            subprocess.run(['git', 'add', filepath], check=True)
            
            # 커밋 체크 (변경사항이 있는지 확인)
            result = subprocess.run(['git', 'diff', '--staged', '--quiet'], capture_output=True)
            if result.returncode != 0:  # 변경사항이 있음
                # 커밋
                commit_message = f"🤖 Auto-post: {os.path.basename(filepath)}"
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                
                # 푸시
                subprocess.run(['git', 'push'], check=True)
                print("✅ Git 커밋 및 푸시 완료!")
                return True
            else:
                print("ℹ️ 변경사항이 없어 커밋하지 않습니다.")
                return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Git 오류: {e}")
            return False
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return False

    def run(self):
        """메인 실행 함수"""
        print("🚀 간단한 테스트 블로거 시작!")
        print("=" * 50)
        
        # 블로그 포스트 생성
        post_data = self.generate_blog_post()
        
        # 파일 생성
        filepath = self.create_post_file(post_data)
        if not filepath:
            print("❌ 파일 생성 실패")
            sys.exit(1)
        
        # Git 커밋 및 푸시
        success = self.git_commit_and_push(filepath)
        if success:
            print("🎉 자동 포스팅 완료!")
            print(f"📝 제목: {post_data['title']}")
            print(f"📂 카테고리: {post_data['category']}")
            print(f"📄 파일: {os.path.basename(filepath)}")
        else:
            print("⚠️ 포스트는 생성되었지만 Git 푸시 실패")
        
        print("=" * 50)

if __name__ == "__main__":
    blogger = SimpleBlogger()
    blogger.run()
