#!/usr/bin/env python3
"""
🤖 AI 자동 블로그 포스팅 시스템
매일 자동으로 AI 관련 고품질 블로그 포스트를 생성합니다.
GitHub Pages Jekyll 블로그 완벽 지원
"""

import os
import json
import random
from datetime import datetime, timedelta
from openai import OpenAI
import subprocess
import sys

class AutoBlogger:
    def __init__(self):
        """초기화 및 OpenAI 클라이언트 설정"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.posts_dir = "_posts"
        self.ensure_posts_directory()
        
        # AI 관련 주제 목록
        self.topics = [
            "ChatGPT 활용법",
            "머신러닝 기초",
            "딥러닝 트렌드",
            "AI 도구 소개",
            "프롬프트 엔지니어링",
            "AI 윤리와 미래",
            "자연어처리 기술",
            "컴퓨터 비전",
            "AI 프로그래밍 튜토리얼",
            "생성형 AI 활용",
            "AI 비즈니스 적용사례",
            "오픈소스 AI 도구"
        ]
        
        # 카테고리 매핑
        self.category_mapping = {
            "ChatGPT": ["ChatGPT 활용법", "프롬프트 엔지니어링", "생성형 AI 활용"],
            "Machine Learning": ["머신러닝 기초", "딥러닝 트렌드", "자연어처리 기술", "컴퓨터 비전"],
            "AI Tools": ["AI 도구 소개", "오픈소스 AI 도구"],
            "Programming": ["AI 프로그래밍 튜토리얼"],
            "Business": ["AI 비즈니스 적용사례"],
            "Ethics": ["AI 윤리와 미래"]
        }

    def ensure_posts_directory(self):
        """포스트 디렉토리 확인 및 생성"""
        if not os.path.exists(self.posts_dir):
            os.makedirs(self.posts_dir)
            print(f"✅ {self.posts_dir} 디렉토리를 생성했습니다.")

    def get_category_for_topic(self, topic):
        """주제에 따른 카테고리 결정"""
        for category, topics in self.category_mapping.items():
            if topic in topics:
                return category
        return "AI General"

    def generate_blog_post(self):
        """GPT-4를 사용하여 블로그 포스트 생성"""
        topic = random.choice(self.topics)
        category = self.get_category_for_topic(topic)
        
        print(f"🤖 주제: {topic}")
        print(f"📂 카테고리: {category}")
        
        # GPT-4 프롬프트
        prompt = f"""
        다음 주제로 전문적이고 실용적인 블로그 포스트를 한국어로 작성해주세요:

        주제: {topic}
        
        요구사항:
        1. 800-1200단어 분량
        2. 초보자도 이해할 수 있도록 친근하게 설명
        3. 구체적인 예시와 실습 내용 포함
        4. 마크다운 형식으로 작성
        5. 코드 예제가 필요한 경우 포함
        6. 실용적이고 바로 적용 가능한 내용
        
        구조:
        - 흥미로운 도입부
        - 주요 개념 설명
        - 실제 사용 예시
        - 단계별 가이드
        - 팁과 주의사항
        - 마무리 및 다음 단계 제안
        
        블로그 포스트 제목과 내용을 생성해주세요.
        """
        
        try:
            print("🔄 GPT-4로 콘텐츠를 생성 중...")
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 AI와 기술에 특화된 전문 블로거입니다. 복잡한 기술을 쉽고 재미있게 설명하는 것이 특기입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # 제목 추출 (첫 번째 # 헤더)
            lines = content.split('\n')
            title = "AI 인사이트 블로그"
            for line in lines:
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    break
            
            return {
                'title': title,
                'content': content,
                'topic': topic,
                'category': category
            }
            
        except Exception as e:
            print(f"❌ OpenAI API 오류: {e}")
            return None

    def create_post_file(self, post_data):
        """Jekyll 형식의 마크다운 파일 생성"""
        if not post_data:
            return None
            
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # 파일명 생성 (한글 제목을 영문으로 변환)
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
        # 한글과 특수문자를 영문으로 변환
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        safe_title = ""
        
        for char in title:
            if char in safe_chars:
                safe_title += char
            elif char == ' ':
                safe_title += '-'
        
        # 연속된 하이픈 제거 및 길이 제한
        safe_title = '-'.join(filter(None, safe_title.split('-')))
        return safe_title[:50] if len(safe_title) > 50 else safe_title

    def git_commit_and_push(self, filepath):
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
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return False

    def run(self):
        """메인 실행 함수"""
        print("🚀 AI 자동 블로거 시작!")
        print("=" * 50)
        
        # API 키 확인
        if not os.getenv('OPENAI_API_KEY'):
            print("❌ OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
            sys.exit(1)
        
        # 블로그 포스트 생성
        post_data = self.generate_blog_post()
        if not post_data:
            print("❌ 포스트 생성 실패")
            sys.exit(1)
        
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
    blogger = AutoBlogger()
    blogger.run()
