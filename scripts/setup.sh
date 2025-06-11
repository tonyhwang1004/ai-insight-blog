#!/bin/bash

# AI 인사이트 블로그 환경 설정 스크립트
# Author: AI Insight Blog Team
# Created: 2025-06-11

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI 인사이트 블로그 자동 포스팅 환경 설정 시작${NC}"
echo "=================================================="

# Python 버전 확인
echo -e "${YELLOW}📋 Python 버전 확인...${NC}"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
    echo -e "${GREEN}✅ $python_version${NC}"
else
    echo -e "${RED}❌ Python3가 설치되지 않았습니다.${NC}"
    echo -e "${YELLOW}설치 방법:${NC}"
    echo -e "${YELLOW}  Ubuntu/Debian: sudo apt install python3 python3-pip${NC}"
    echo -e "${YELLOW}  CentOS/RHEL: sudo yum install python3 python3-pip${NC}"
    echo -e "${YELLOW}  macOS: brew install python3${NC}"
    exit 1
fi

# pip 확인
echo -e "${YELLOW}📦 pip 확인 및 업그레이드...${NC}"
if command -v pip3 &> /dev/null; then
    python3 -m pip install --upgrade pip
    echo -e "${GREEN}✅ pip 업그레이드 완료${NC}"
else
    echo -e "${RED}❌ pip3가 설치되지 않았습니다.${NC}"
    exit 1
fi

# 가상환경 생성 여부 확인
echo -e "${BLUE}🤔 가상환경을 생성하시겠습니까?${NC}"
echo -e "${YELLOW}   가상환경을 사용하면 시스템 Python과 분리되어 더 안전합니다.${NC}"
read -p "가상환경 생성 (y/n): " create_venv

if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo -e "${YELLOW}🔧 가상환경 생성 중...${NC}"
    
    if python3 -m venv ai_blog_env; then
        echo -e "${GREEN}✅ 가상환경 'ai_blog_env' 생성 완료${NC}"
        
        # 가상환경 활성화
        source ai_blog_env/bin/activate
        echo -e "${GREEN}✅ 가상환경 활성화 완료${NC}"
        echo -e "${YELLOW}💡 다음번 사용시: source ai_blog_env/bin/activate${NC}"
    else
        echo -e "${RED}❌ 가상환경 생성 실패${NC}"
        exit 1
    fi
fi

# 필요한 패키지 설치
echo -e "${YELLOW}📦 필요한 Python 패키지 설치 중...${NC}"
packages=("openai>=1.0.0" "requests>=2.31.0" "beautifulsoup4>=4.12.0" "schedule>=1.2.0")

for package in "${packages[@]}"; do
    package_name=$(echo "$package" | cut -d'>' -f1 | cut -d'=' -f1)
    echo -e "${YELLOW}  설치 중: $package_name${NC}"
    
    if python3 -m pip install "$package"; then
        echo -e "${GREEN}  ✅ $package_name 설치 완료${NC}"
    else
        echo -e "${RED}  ❌ $package_name 설치 실패${NC}"
        echo -e "${YELLOW}  수동 설치 시도: pip3 install $package${NC}"
    fi
done

# OpenAI API 키 설정
echo -e "${YELLOW}🔑 OpenAI API 키 설정${NC}"
echo -e "${BLUE}   OpenAI API 키가 필요합니다. https://platform.openai.com/api-keys 에서 발급받으세요.${NC}"
read -p "OpenAI API 키 입력 (Enter로 건너뛰기): " api_key

if [[ -n "$api_key" ]]; then
    # .env 파일에 저장
    echo "OPENAI_API_KEY=$api_key" > .env
    echo -e "${GREEN}✅ API 키가 .env 파일에 저장되었습니다${NC}"
    
    # bashrc에도 추가할지 확인
    echo -e "${BLUE}🤔 bashrc에 영구적으로 추가하시겠습니까?${NC}"
    echo -e "${YELLOW}   (새 터미널에서도 자동으로 설정됩니다)${NC}"
    read -p "bashrc에 추가 (y/n): " add_to_bashrc
    
    if [[ $add_to_bashrc == "y" || $add_to_bashrc == "Y" ]]; then
        if ! grep -q "OPENAI_API_KEY" ~/.bashrc; then
            echo "export OPENAI_API_KEY='$api_key'" >> ~/.bashrc
            echo -e "${GREEN}✅ API 키가 ~/.bashrc에 추가되었습니다${NC}"
            echo -e "${YELLOW}💡 새 터미널에서 적용: source ~/.bashrc${NC}"
        else
            echo -e "${YELLOW}⚠️ API 키가 이미 ~/.bashrc에 있습니다${NC}"
        fi
    fi
    
    # 현재 세션에 적용
    export OPENAI_API_KEY="$api_key"
    echo -e "${GREEN}✅ API 키가 현재 세션에 설정되었습니다${NC}"
else
    echo -e "${YELLOW}⚠️ API 키를 나중에 설정하세요:${NC}"
    echo -e "${YELLOW}   export OPENAI_API_KEY='your-api-key-here'${NC}"
    echo -e "${YELLOW}   또는 .env 파일에 OPENAI_API_KEY=your-key 추가${NC}"
fi

# 디렉토리 구조 생성
echo -e "${YELLOW}📁 프로젝트 디렉토리 구조 생성...${NC}"
directories=("posts" "logs" "assets/css" "assets/js" "assets/images")

for dir in "${directories[@]}"; do
    if mkdir -p "$dir"; then
        echo -e "${GREEN}  ✅ $dir/${NC}"
    else
        echo -e "${RED}  ❌ $dir 생성 실패${NC}"
    fi
done

# 실행 권한 부여
echo -e "${YELLOW}🔧 스크립트 실행 권한 설정...${NC}"
if [[ -f "scripts/auto_blogger.py" ]]; then
    chmod +x scripts/auto_blogger.py
    echo -e "${GREEN}✅ auto_blogger.py 실행 권한 부여${NC}"
fi

if [[ -f "scripts/setup.sh" ]]; then
    chmod +x scripts/setup.sh
    echo -e "${GREEN}✅ setup.sh 실행 권한 부여${NC}"
fi

# 테스트 실행
echo -e "${BLUE}🧪 설치 테스트를 진행하시겠습니까?${NC}"
read -p "테스트 실행 (y/n): " run_test

if [[ $run_test == "y" || $run_test == "Y" ]]; then
    echo -e "${YELLOW}🧪 패키지 import 테스트 중...${NC}"
    
    python3 -c "
import sys
try:
    import openai
    print('✅ openai 패키지 정상')
except ImportError as e:
    print(f'❌ openai 패키지 오류: {e}')
    sys.exit(1)

try:
    import requests
    print('✅ requests 패키지 정상')
except ImportError as e:
    print(f'❌ requests 패키지 오류: {e}')
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    print('✅ beautifulsoup4 패키지 정상')
except ImportError as e:
    print(f'❌ beautifulsoup4 패키지 오류: {e}')
    sys.exit(1)

print('🎉 모든 패키지가 정상적으로 설치되었습니다!')
"
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ 모든 테스트 통과!${NC}"
    else
        echo -e "${RED}❌ 일부 테스트 실패${NC}"
    fi
fi

# 크론탭 설정 안내
echo -e "${YELLOW}⏰ 자동 실행 설정 (크론탭) 안내${NC}"
echo -e "${BLUE}=================================================${NC}"
echo -e "${YELLOW}정기적인 자동 포스팅을 위해 크론탭을 설정할 수 있습니다.${NC}"
echo -e "${YELLOW}예시) 매일 오전 9시에 자동 실행:${NC}"
echo -e "${GREEN}1. crontab -e${NC}"
echo -e "${GREEN}2. 다음 줄 추가:${NC}"
echo -e "${GREEN}   0 9 * * * cd $(pwd) && python3 scripts/auto_blogger.py >> logs/cron.log 2>&1${NC}"
echo ""

# 완료 메시지
echo -e "${GREEN}🎉 환경 설정 완료!${NC}"
echo -e "${BLUE}=================================================${NC}"
echo -e "${YELLOW}💡 사용 방법:${NC}"
echo -e "${GREEN}  수동 실행: python3 scripts/auto_blogger.py${NC}"
echo -e "${GREEN}  로그 확인: tail -f logs/auto_blogger.log${NC}"
echo -e "${GREEN}  가상환경 활성화: source ai_blog_env/bin/activate${NC}"
echo ""
echo -e "${YELLOW}📚 추가 정보:${NC}"
echo -e "${BLUE}  프로젝트 URL: https://github.com/tonyhwang1004/ai-insight-blog${NC}"
echo -e "${BLUE}  블로그 URL: https://tonyhwang1004.github.io/ai-insight-blog${NC}"
echo ""
echo -e "${GREEN}Happy Blogging! 🚀${NC}"
