#!/usr/bin/env python3
"""
🧪 초간단 테스트 블로거 (의존성 제로)
"""

import os
import random
from datetime import datetime
import subprocess
import sys

def ensure_posts_directory():
    """포스트 디렉토리 생성"""
    posts_dir = "_posts"
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
        print(f"✅ {posts_dir} 디렉토리를 생성했습니다.")
    return posts_dir

def get_blog_content():
    """미리 준비된 블로그 콘텐츠"""
    contents = [
        {
            'title': 'AI 시대의 새로운 기회: 개발자를 위한 5가지 준비사항',
            'content': '''# AI 시대의 새로운 기회

## 🚀 들어가며
인공지능 기술이 급속도로 발전하면서 개발자들에게 새로운 기회와 도전이 동시에 찾아오고 있습니다.

## 1. 머신러닝 기초 학습 🤖
AI 개발의 첫걸음은 머신러닝 기초를 이해하는 것입니다.

### 핵심 기술 스택
- **Python**: 가장 널리 사용되는 AI 개발 언어
- **TensorFlow/PyTorch**: 딥러닝 프레임워크
- **Scikit-learn**: 전통적인 머신러닝 라이브러리

### 학습 로드맵
1. Python 기초 문법 익히기
2. 통계학과 선형대수 기본 개념 학습
3. 머신러닝 알고리즘 이해
4. 실습 프로젝트 진행

## 2. 데이터 처리 능력 향상 📊
AI의 핵심은 데이터입니다. 좋은 데이터 없이는 좋은 AI 모델을 만들 수 없습니다.

## 3. API 활용 능력 📡
최신 AI 서비스들은 대부분 API 형태로 제공됩니다.

## 4. 윤리적 AI 개발 🔍
AI 기술이 발전할수록 윤리적 고려사항이 중요해집니다.

## 5. 지속적인 학습과 네트워킹 🌐
AI 분야는 빠르게 변화하므로 지속적인 학습이 필수입니다.

## 마무리 💡
AI 시대는 이미 시작되었고, 준비된 개발자에게는 무한한 기회가 있습니다.''',
            'category': 'AI General',
            'topic': 'AI 개발자 준비사항'
        },
        {
            'title': 'ChatGPT 프롬프트 엔지니어링 완벽 가이드',
            'content': '''# ChatGPT 프롬프트 엔지니어링 완벽 가이드

## 🎯 프롬프트 엔지니어링이란?
프롬프트 엔지니어링은 AI 모델에게 더 정확하고 유용한 답변을 얻기 위해 질문을 체계적으로 설계하는 기술입니다.

## 핵심 원칙들

### 1. 명확하고 구체적으로 질문하기
모호한 질문보다는 구체적인 요구사항을 제시하세요.

### 2. 컨텍스트 제공하기
배경 정보와 상황을 명확히 설명하세요.

### 3. 단계별 접근법 활용
복잡한 문제는 작은 단위로 분해하여 접근하세요.

## 실용적인 프롬프트 템플릿

### 기본 구조
```
역할: [AI에게 부여할 역할]
맥락: [상황과 배경 정보]  
작업: [구체적인 요청사항]
형식: [원하는 답변 형태]
```

## 고급 기법들

### Few-shot Learning
예시를 통해 원하는 답변 형태를 보여주세요.

### Chain of Thought
단계별 사고 과정을 요청하세요.

## 마무리
프롬프트 엔지니어링은 AI 시대의 필수 스킬입니다.''',
            'category': 'ChatGPT',
            'topic': '프롬프트 엔지니어링'
        }
    ]
    return random.choice(contents)

def make_safe_filename(title):
    """안전한 파일명 생성"""
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    safe_title = ""
    
    for char in title:
        if char in safe_chars:
            safe_title += char
        elif char == ' ':
            safe_title += '-'
    
    # 연속된 하이픈 제거
    while '--' in safe_title:
        safe_title = safe_title.replace('--', '-')
    
    safe_title = safe_title.strip('-')
    return safe_title[:50] if len(safe_title) > 50 else safe_title or "ai-blog-post"

def create_post_file(posts_dir, post_data):
    """마크다운 파일 생성"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # 파일명 생성
    safe_title = make_safe_filename(post_data['title'])
    filename = f"{date_str}-{safe_title}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # Jekyll Front Matter
    front_matter = f"""---
layout: post
title: "{post_data['title']}"
date: {date_str} {time_str} +0900
categories: [{post_data['category']}]
tags: [AI, {post_data['topic']}, 인공지능, 기술]
author: "AI Insight Blog"
description: "{post_data['title']} - 실용적인 AI 가이드와 최신 트렌드"
---

"""
    
    # 파일 저장
    full_content = front_matter + post_data['content']
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        print(f"✅ 포스트 생성: {filename}")
        return filepath
    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")
        return None

def git_commit_push(filepath):
    """Git 커밋 및 푸시"""
    try:
        # Git 설정
        subprocess.run(['git', 'config', '--global', 'user.name', 'AI Blogger Bot'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'ai-blogger@github-actions.com'], check=True)
        
        # 파일 추가
        subprocess.run(['git', 'add', filepath], check=True)
        
        # 커밋
        commit_message = f"🤖 Auto-post: {os.path.basename(filepath)}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 푸시
        subprocess.run(['git', 'push'], check=True)
        
        print("✅ Git 커밋 및 푸시 완료!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 초간단 테스트 블로거 시작!")
    print("=" * 50)
    
    # 포스트 디렉토리 생성
    posts_dir = ensure_posts_directory()
    
    # 블로그 콘텐츠 선택
    post_data = get_blog_content()
    print(f"📝 제목: {post_data['title']}")
    print(f"📂 카테고리: {post_data['category']}")
    
    # 파일 생성
    filepath = create_post_file(posts_dir, post_data)
    if not filepath:
        print("❌ 파일 생성 실패")
        sys.exit(1)
    
    # Git 처리
    success = git_commit_push(filepath)
    if success:
        print("🎉 자동 포스팅 완료!")
    else:
        print("⚠️ 포스트는 생성되었지만 Git 푸시 실패")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
