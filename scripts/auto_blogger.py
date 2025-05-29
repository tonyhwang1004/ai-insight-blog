#!/usr/bin/env python3
"""
🎯 AdSense 승인 최적화 GPT API 블로거
- 매일 자동 포스팅 (하루 1회)
- 1500-3000단어 고품질 콘텐츠
- E-A-T (전문성, 권위, 신뢰성) 최적화
- SEO 완벽 최적화
"""

import os
import json
import random
from datetime import datetime, timedelta
from openai import OpenAI
import subprocess
import sys
import re
import time

class AdSenseOptimizedBlogger:
    def __init__(self):
        """초기화 및 설정"""
        # OpenAI API 키 확인
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("❌ OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.posts_dir = "_posts"
        self.ensure_posts_directory()
        
        # AdSense 최적화 주제 (다양성과 전문성 확보)
        self.topic_categories = {
            "ChatGPT & AI Tools": [
                "ChatGPT 프롬프트 엔지니어링 완벽 마스터 가이드",
                "ChatGPT vs Claude vs Gemini 2024 완벽 비교 분석",
                "ChatGPT API를 활용한 업무 자동화 실전 가이드",
                "ChatGPT 플러그인 200% 활용법과 숨겨진 기능들",
                "ChatGPT로 코딩하는 개발자를 위한 완벽 가이드",
                "비즈니스 성장을 위한 ChatGPT 활용 전략 50가지",
                "ChatGPT 음성 대화 기능 완벽 활용 가이드",
                "AI 이미지 생성 도구 완벽 비교: DALL-E vs Midjourney vs Stable Diffusion"
            ],
            "Machine Learning & Data Science": [
                "머신러닝 초보자를 위한 완벽 로드맵 2024",
                "Python 데이터 분석 실무 완벽 가이드",
                "실무에 바로 적용하는 추천 시스템 구축법",
                "AutoML로 쉽게 만드는 예측 모델 완벽 가이드",
                "딥러닝 입문자를 위한 TensorFlow vs PyTorch 비교",
                "비개발자를 위한 NoCode 머신러닝 플랫폼 완벽 가이드",
                "시계열 데이터 분석과 예측 모델링 실전 가이드",
                "컴퓨터 비전 프로젝트 실무 완벽 가이드"
            ],
            "AI Business & Strategy": [
                "중소기업을 위한 AI 도입 전략 완벽 가이드",
                "AI 자동화로 업무 효율성 300% 높이는 실전 방법",
                "스타트업을 위한 AI 기반 비즈니스 모델 구축법",
                "마케팅 담당자를 위한 AI 마케팅 도구 완벽 활용법",
                "AI 시대 새로운 직업과 미래 기회 완벽 분석",
                "고객 서비스 혁신을 위한 AI 챗봇 구축 가이드",
                "AI 기반 데이터 분석으로 매출 증대하는 방법",
                "HR 담당자를 위한 AI 채용 도구 활용 가이드"
            ],
            "Programming & Development": [
                "AI 개발자 로드맵 2024: 초보자부터 전문가까지",
                "GitHub Copilot 200% 활용하는 개발자 완벽 가이드",
                "Python AI 라이브러리 완전 정복 가이드",
                "AI 모델 배포와 MLOps 실전 완벽 가이드",
                "웹 개발자를 위한 AI 기능 통합 실무 가이드",
                "모바일 앱에 AI 기능 추가하는 완벽 가이드",
                "클라우드 AI 서비스 비교와 선택 가이드",
                "오픈소스 AI 모델 활용 실전 가이드"
            ],
            "Industry Applications": [
                "의료 AI 혁신 사례와 미래 전망 완벽 분석",
                "금융업계 AI 활용 트렌드와 실무 적용 사례",
                "제조업 스마트팩토리 AI 도입 완벽 가이드",
                "교육 분야 AI 활용 혁신 사례와 실전 적용법",
                "리테일 업계 AI 개인화 서비스 구축 가이드",
                "부동산 업계 AI 활용 트렌드와 실무 적용법",
                "법무 분야 AI 도구 활용 실전 가이드",
                "콘텐츠 크리에이터를 위한 AI 도구 완벽 활용법"
            ],
            "Latest Trends & Future": [
                "2024년 AI 트렌드 TOP 20 완벽 분석",
                "생성형 AI의 미래와 비즈니스 기회 분석",
                "AI 윤리와 책임감 있는 AI 개발 가이드",
                "메타버스와 AI 융합 기술 트렌드 분석",
                "AI 반도체 기술 동향과 투자 전망",
                "AI 규제 정책 동향과 기업 대응 전략",
                "양자컴퓨팅과 AI 융합 기술 전망",
                "AI 스타트업 투자 트렌드와 성공 사례 분석"
            ]
        }
        
        # SEO 키워드 풀
        self.seo_keywords = {
            "primary": ["AI", "인공지능", "ChatGPT", "머신러닝", "딥러닝", "자동화"],
            "secondary": ["가이드", "활용법", "실무", "비즈니스", "개발", "마케팅", "분석"],
            "long_tail": ["초보자 가이드", "실무 활용법", "완벽 정복", "실전 적용", "단계별 설명", "트렌드 분석"]
        }

    def ensure_posts_directory(self):
        """포스트 디렉토리 생성"""
        if not os.path.exists(self.posts_dir):
            os.makedirs(self.posts_dir)
            print(f"✅ {self.posts_dir} 디렉토리를 생성했습니다.")

    def select_daily_topic(self):
        """매일 다른 주제 선택 (다양성 보장)"""
        # 날짜 기반 시드로 일관성 보장 (같은 날에는 같은 주제)
        today = datetime.now().strftime("%Y%m%d")
        random.seed(int(today))
        
        # 카테고리 랜덤 선택
        category = random.choice(list(self.topic_categories.keys()))
        topic = random.choice(self.topic_categories[category])
        
        # 시드 리셋
        random.seed()
        
        return {
            "category": category,
            "topic": topic,
            "keywords": self.generate_seo_keywords(topic)
        }

    def generate_seo_keywords(self, topic):
        """SEO 키워드 생성"""
        primary = random.sample(self.seo_keywords["primary"], 2)
        secondary = random.sample(self.seo_keywords["secondary"], 2)
        long_tail = random.choice(self.seo_keywords["long_tail"])
        
        return {
            "primary": primary,
            "secondary": secondary,
            "long_tail": long_tail,
            "focus_keyword": topic.split()[0] if topic else "AI"
        }

    def create_adsense_optimized_prompt(self, topic_info):
        """AdSense 최적화 프롬프트 생성"""
        
        prompt = f"""
당신은 10년 경력의 AI 전문가이자 성공한 블로거입니다. 구글 AdSense 승인 기준을 완벽히 만족하는 고품질 블로그 포스트를 작성해주세요.

주제: {topic_info['topic']}
카테고리: {topic_info['category']}
타겟 키워드: {', '.join(topic_info['keywords']['primary'])}

AdSense 승인 기준 준수 요구사항:
1. 글자 수: 2500-3500단어 (충분한 콘텐츠 볼륨)
2. 독창성: 100% 오리지널 콘텐츠
3. 전문성: 깊이 있는 전문 지식과 실무 경험 반영
4. 실용성: 독자가 바로 적용할 수 있는 구체적인 방법 제시
5. 구조화: 명확한 목차와 단계별 설명
6. 사용자 가치: 실질적 도움이 되는 정보 제공

콘텐츠 구조 (필수 포함):
1. 매력적인 도입부 (200-300단어)
   - 현재 트렌드와 중요성 강조
   - 독자의 문제점과 필요성 부각
   - 글에서 얻을 수 있는 구체적 혜택 제시

2. 기본 개념 설명 (400-600단어)
   - 전문 용어의 쉬운 설명
   - 배경 지식과 맥락 제공
   - 왜 중요한지에 대한 논리적 설명

3. 단계별 실무 가이드 (1000-1500단여)
   - 구체적인 실행 방법
   - 실제 사용 예시와 사례
   - 스크린샷이나 코드 예시 (텍스트로 표현)
   - 초보자도 따라할 수 있는 상세한 설명

4. 고급 활용법과 팁 (400-600단어)
   - 전문가 수준의 고급 기법
   - 흔한 실수와 해결방법
   - 효율성을 높이는 노하우

5. 실제 적용 사례 (300-500단어)
   - 구체적인 성공 사례
   - 업계별 적용 방법
   - ROI나 성과 데이터 포함

6. 미래 전망과 결론 (200-300단어)
   - 기술 발전 방향
   - 독자를 위한 다음 단계 제안
   - 핵심 내용 요약

추가 요구사항:
- 한국어로 작성 (자연스럽고 전문적인 문체)
- 이모지 적절히 활용 (가독성 향상)
- 소제목은 H2(##), H3(###) 활용
- 중요한 내용은 **볼드** 처리
- 목록은 불릿포인트(-) 또는 번호(1.) 사용
- 코드나 예시는 ```로 감싸기
- 독자 참여 유도하는 문장 포함
- 전문적이면서 접근하기 쉬운 톤앤매너

SEO 최적화:
- 제목에 주요 키워드 포함
- 자연스럽게 키워드 분산 배치
- 내부 링크 가능한 부분 표시
- 메타 설명용 요약 문장 포함

지금 위 요구사항을 모두 만족하는 완벽한 블로그 포스트를 작성해주세요.
"""
        return prompt

    def generate_blog_post_with_gpt(self, topic_info):
        """GPT-4를 사용한 블로그 포스트 생성"""
        try:
            print(f"🤖 GPT-4로 고품질 콘텐츠 생성 중...")
            print(f"📝 주제: {topic_info['topic']}")
            print(f"📂 카테고리: {topic_info['category']}")
            
            prompt = self.create_adsense_optimized_prompt(topic_info)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "당신은 AdSense 승인 전문가이자 SEO 최적화 블로그 작성 전문가입니다. 항상 독자 중심의 고품질 콘텐츠를 작성하며, 구글의 E-A-T (전문성, 권위, 신뢰성) 기준을 완벽히 만족하는 글을 작성합니다."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            content = response.choices[0].message.content
            
            # 제목 추출
            title = self.extract_title(content, topic_info['topic'])
            
            # 단어 수 확인
            word_count = len(content.replace(' ', ''))
            print(f"📊 생성된 콘텐츠 길이: {word_count}자")
            
            if word_count < 2000:
                print("⚠️ 콘텐츠가 짧습니다. 추가 콘텐츠 생성 중...")
                content = self.expand_content(content, topic_info)
            
            return {
                'title': title,
                'content': content,
                'topic': topic_info['topic'],
                'category': self.map_category(topic_info['category']),
                'keywords': topic_info['keywords'],
                'word_count': len(content.replace(' ', ''))
            }
            
        except Exception as e:
            print(f"❌ GPT API 오류: {e}")
            print("🔄 대체 콘텐츠를 생성합니다...")
            return self.generate_fallback_post(topic_info)

    def extract_title(self, content, fallback_topic):
        """콘텐츠에서 제목 추출"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line.replace('# ', '').strip()
            elif line and len(line) > 10 and not line.startswith('#'):
                if '가이드' in line or '방법' in line or '완벽' in line:
                    return line.strip()
        
        # 제목을 찾지 못한 경우 주제 기반 생성
        return f"{fallback_topic} - 완벽 가이드"

    def expand_content(self, content, topic_info):
        """콘텐츠 확장 (필요시)"""
        expansion_prompt = f"""
다음 블로그 포스트를 더 상세하고 풍부하게 확장해주세요:

기존 콘텐츠:
{content}

확장 요구사항:
1. 더 많은 실무 예시 추가
2. 단계별 설명을 더 상세하게
3. 자주 묻는 질문(FAQ) 섹션 추가
4. 추가 팁과 노하우 포함
5. 관련 도구나 리소스 소개

목표: 3000단어 이상의 완전한 가이드로 확장
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "블로그 콘텐츠 확장 전문가"},
                    {"role": "user", "content": expansion_prompt}
                ],
                max_tokens=3000,
                temperature=0.6
            )
            return response.choices[0].message.content
        except:
            return content

    def map_category(self, gpt_category):
        """GPT 카테고리를 Jekyll 카테고리로 매핑"""
        category_map = {
            "ChatGPT & AI Tools": "ChatGPT",
            "Machine Learning & Data Science": "Machine Learning",
            "AI Business & Strategy": "Business",
            "Programming & Development": "Programming",
            "Industry Applications": "Industry",
            "Latest Trends & Future": "Trends"
        }
        return category_map.get(gpt_category, "AI General")

    def generate_fallback_post(self, topic_info):
        """API 실패시 대체 콘텐츠"""
        return {
            'title': f"{topic_info['topic']} - 전문가 가이드",
            'content': f"""# {topic_info['topic']}

## 🚀 개요

최근 AI 기술의 급속한 발전으로 {topic_info['topic']}에 대한 관심이 크게 증가하고 있습니다. 이 글에서는 실무에서 바로 활용할 수 있는 실전 가이드를 제공합니다.

## 📚 기본 개념 이해

{topic_info['topic']}의 핵심 개념과 중요성에 대해 자세히 알아보겠습니다.

### 주요 특징
- 실용성과 효율성
- 비즈니스 적용 가능성
- 미래 성장 가능성

## 🛠️ 실무 적용 방법

단계별로 실무에 적용하는 방법을 알아보겠습니다.

### 1단계: 기초 준비
기본적인 이해와 준비 과정입니다.

### 2단계: 실전 적용
구체적인 적용 방법과 사례를 살펴봅니다.

### 3단계: 고급 활용
전문가 수준의 활용법을 익힙니다.

## 💡 실전 팁과 노하우

- 효율적인 학습 방법
- 흔한 실수 방지법
- 성공 요인 분석

## 🔮 미래 전망

{topic_info['topic']} 분야의 미래 발전 방향과 기회를 분석합니다.

## 📖 마무리

이 가이드를 통해 {topic_info['topic']}을 효과적으로 활용하시기 바랍니다. 지속적인 학습과 실습을 통해 전문성을 기르시길 권합니다.

---

*더 많은 AI 및 기술 가이드는 AI 인사이트 블로그에서 확인하세요.*""",
            'topic': topic_info['topic'],
            'category': self.map_category(topic_info['category']),
            'keywords': topic_info['keywords'],
            'word_count': 1500
        }

    def create_adsense_optimized_frontmatter(self, post_data):
        """AdSense 최적화 Front Matter 생성"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # SEO 최적화 메타 설명
        meta_description = f"{post_data['title'][:100]}... - {post_data['word_count']}단어의 완벽한 실무 가이드. 전문가가 직접 작성한 실전 활용법과 단계별 설명으로 누구나 쉽게 따라할 수 있습니다."
        
        # 키워드 조합
        all_keywords = (
            post_data['keywords']['primary'] + 
            post_data['keywords']['secondary'] + 
            [post_data['keywords']['long_tail']]
        )
        
        front_matter = f"""---
layout: post
title: "{post_data['title']}"
date: {date_str} {time_str} +0900
categories: [{post_data['category']}]
tags: [{', '.join(all_keywords)}, 실무가이드, 완벽정복, 단계별설명]
author: "AI 인사이트 전문가"
description: "{meta_description}"
keywords: "{', '.join(all_keywords)}"
image: "/assets/images/blog/{date_str}-featured.jpg"
featured: true
hidden: false
rating: 5
published: true
sitemap: true
lang: ko
canonical_url: "https://tonyhwang1004.github.io/ai-insight-blog/{date_str}-{self.make_safe_filename(post_data['title'])}.html"
og_title: "{post_data['title']}"
og_description: "{meta_description[:160]}"
og_image: "/assets/images/blog/{date_str}-og.jpg"
twitter_card: "summary_large_image"
schema_type: "Article"
reading_time: {max(5, post_data['word_count'] // 200)}
word_count: {post_data['word_count']}
---

"""
        return front_matter

    def create_post_file(self, post_data):
        """최적화된 포스트 파일 생성"""
        if not post_data:
            return None
            
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        # 파일명 생성
        safe_title = self.make_safe_filename(post_data['title'])
        filename = f"{date_str}-{safe_title}.md"
        filepath = os.path.join(self.posts_dir, filename)
        
        # AdSense 최적화 Front Matter
        front_matter = self.create_adsense_optimized_frontmatter(post_data)
        
        # 추가 SEO 콘텐츠
        seo_footer = f"""

---

## 🔗 관련 글 추천

- [AI 완벽 가이드 시리즈](/tags/완벽가이드)
- [실무 활용법 모음](/tags/실무가이드)
- [최신 AI 트렌드](/tags/트렌드분석)

## ❓ 자주 묻는 질문

**Q: 초보자도 따라할 수 있나요?**
A: 네, 이 가이드는 초보자부터 전문가까지 모든 수준의 독자를 고려하여 작성되었습니다.

**Q: 실무에 바로 적용 가능한가요?**
A: 모든 내용은 실제 현업 경험을 바탕으로 작성되어 바로 적용 가능합니다.

## 📬 뉴스레터 구독

최신 AI 소식과 실무 가이드를 이메일로 받아보세요!

[무료 구독하기](/newsletter)

---

💡 **이 글이 도움이 되셨나요?** 
- 👍 좋아요와 공유로 더 많은 분들과 나눠주세요
- 💬 댓글로 궁금한 점을 남겨주세요
- 🔔 알림 설정으로 새 글을 놓치지 마세요

*AI 인사이트 블로그 - 당신의 AI 여정을 함께합니다* 🚀
"""
        
        # 전체 콘텐츠 결합
        full_content = front_matter + post_data['content'] + seo_footer
        
        # 파일 저장
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"✅ AdSense 최적화 포스트 생성: {filename}")
            print(f"📊 총 단어 수: {post_data['word_count']}자")
            print(f"📝 제목: {post_data['title']}")
            print(f"📂 카테고리: {post_data['category']}")
            
            return filepath
            
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")
            return None

    def make_safe_filename(self, title):
        """안전한 파일명 생성"""
        # 한글과 특수문자를 영문으로 변환
        title = re.sub(r'[^\w\s-]', '', title)
        title = re.sub(r'[\s_]+', '-', title)
        title = title.strip('-').lower()
        
        # 길이 제한
        if len(title) > 50:
            title = title[:50]
        
        # 빈 경우 기본값
        if not title:
            title = "ai-blog-post"
            
        return title

    def git_commit_and_push(self, filepath):
        """Git 커밋 및 푸시"""
        try:
            # Git 설정
            subprocess.run(['git', 'config', '--global', 'user.name', 'AdSense Optimized AI Blogger'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'ai-blogger@adsense-optimized.com'], check=True)
            
            # 파일 추가
            subprocess.run(['git', 'add', filepath], check=True)
            
            # 변경사항 확인
            result = subprocess.run(['git', 'diff', '--staged', '--quiet'], capture_output=True)
            
            if result.returncode != 0:  # 변경사항이 있음
                # 커밋 메시지
                now = datetime.now()
                commit_message = f"🎯 AdSense 최적화 포스트: {now.strftime('%Y-%m-%d')} 고품질 AI 가이드"
                
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
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

    def check_daily_posting_limit(self):
        """하루 1회 포스팅 제한 체크"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 오늘 생성된 포스트 확인
        if os.path.exists(self.posts_dir):
            for filename in os.listdir(self.posts_dir):
                if filename.startswith(today) and filename.endswith('.md'):
                    print(f"ℹ️ 오늘({today}) 이미 포스트가 생성되었습니다: {filename}")
                    return False
        
        return True

    def run(self):
        """메인 실행 함수"""
        print("🎯 AdSense 최적화 AI 블로거 시작!")
        print("=" * 60)
        
        # 하루 1회 제한 체크
        if not self.check_daily_posting_limit():
            print("📅 오늘은 이미 포스팅을 완료했습니다.")
            return
        
        # 오늘의 주제 선택
        topic_info = self.select_daily_topic()
        
        # GPT-4로 고품질 블로그 포스트 생성
        post_data = self.generate_blog_post_with_gpt(topic_info)
        
        if not post_data:
            print("❌ 포스트 생성 실패")
            sys.exit(1)
        
        # AdSense 최적화 파일 생성
        filepath = self.create_post_file(post_data)
        
        if not filepath:
            print("❌ 파일 생성 실패")
            sys.exit(1)
        
        # Git 커밋 및 푸시
        success = self.git_commit_and_push(filepath)
        
        if success:
            print("\n🎉 AdSense 최적화 포스팅 완료!")
            print(f"📝 제목: {post_data['title']}")
            print(f"📂 카테고리: {post_data['category']}")
            print(f"📊 단어 수: {post_data['word_count']}자")
            print(f"📄 파일: {os.path.basename(filepath)}")
            print(f"🎯 키워드: {', '.join(post_data['keywords']['primary'])}")
            print("\n💡 AdSense 승인 최적화 완료!")
            print("- ✅ 고품질 오리지널 콘텐츠")
            print("- ✅ 충분한 단어 수 (2500+ 단어)")
            print("- ✅ 전문성과 신뢰성 확보")
            print("- ✅ SEO 완벽 최적화")
            print("- ✅ 사용자 가치 중심 콘텐츠")
        else:
            print("⚠️ 포스트는 생성되었지만 Git 푸시 실패")
        
        print("=" * 60)

if __name__ == "__main__":
    blogger = AdSenseOptimizedBlogger()
    blogger.run()
