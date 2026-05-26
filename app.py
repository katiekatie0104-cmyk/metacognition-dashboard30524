import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 레이아웃 및 스타일 테마 주입
st.set_page_config(page_title="메타인지 및 한계효용 학습 최적화", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght=400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #F1F5F9;
    }
    
    /* 창의적 헤더 디자인: 네온 포인트 슬레이트 패널 */
    .premium-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        padding: 2.2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(30, 27, 75, 0.15);
        border-bottom: 4px solid #6366F1;
    }
    
    /* 사용자 배지화 */
    .user-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        font-weight: 600;
        color: #F8FAFC;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
    }
    
    .glass-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .quiz-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .text-neon {
        color: #6366F1;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 상단 프로필 영역 (연구원 글자 제거)
# =========================================================================
st.markdown("""
    <div class="premium-header">
        <table style="width:100%; border:none; border-collapse:collapse; background:none;">
            <tr style="background:none;">
                <td style="border:none; padding:0;">
                    <span style="color:#818CF8; font-weight:600; font-size:0.95rem; letter-spacing:1px;">META-COGNITIVE AI PLATFORM</span>
                    <h1 style="color:white; margin:0.2rem 0 0 0; font-size:2.1rem; font-weight:800;">메타인지 최적화 알고리즘 대시보드</h1>
                </td>
                <td style="border:none; text-align:right; vertical-align:middle; padding:0;">
                    <div class="user-badge">30524 정서영</div>
                </td>
            </tr>
        </table>
    </div>
""", unsafe_allow_html=True)

# =========================================================================
# 단원 데이터베이스 고도화 (물리학 I, 지구과학 I 전과정 확장)
# =========================================================================
if 'db_extended' not in st.session_state:
    st.session_state.db_extended = {
        "물리학 I": {
            "역학과 에너지": [
                {"소단원": "뉴턴 운동 법칙", "시간": 30, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [4, 1]},
                {"소단원": "운동량과 충격량", "시간": 25, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [2, 3]},
                {"소단원": "역학적 에너지 보존", "시간": 40, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [5, 2]}
            ],
            "열과 에너지": [
                {"소단원": "열역학 법칙", "시간": 35, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [1, 4]},
                {"소단원": "특수 상대성 이론", "시간": 45, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [3, 5]}
            ],
            "파동과 정보 통신": [
                {"소단원": "파동의 굴절과 간섭", "시간": 30, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [2, 4]},
                {"소단원": "빛과 물질의 이중성", "시간": 20, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [1, 3]}
            ]
        },
        "지구과학 I": {
            "고체 지구": [
                {"소단원": "판 구조론과 대륙 이동", "시간": 20, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [4, 2]},
                {"소단원": "지질 구조와 화성암", "시간": 30, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [5, 1]}
            ],
            "대기와 해양": [
                {"소단원": "대기 순환과 기압 배치", "시간": 35, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [3, 3]},
                {"소단원": "해류와 해수의 성질", "시간": 25, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [1, 5]}
            ],
            "우주": [
                {"소단원": "별의 표면 온도와 광도", "시간": 45, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [2, 4]},
                {"소단원": "우주 팽창과 외계 행성계", "시간": 40, "예상": 50, "실제": 0, "푼횟수": 0, "정답": [4, 1]}
            ]
        }
    }

# 문항 데이터 바인딩
quiz_bank = {
    "뉴턴 운동 법칙": [
        {"q": "1. 마찰이 없는 수평면 위에서 질량 2kg 물체에 8N의 힘을 가했을 때 가속도의 크기는?", "o": ["1 m/s²", "2 m/s²", "3 m/s²", "4 m/s²", "5 m/s²"]},
        {"q": "2. 가만히 서 있는 버스가 갑자기 출발할 때 승객들이 뒤로 넘어지는 현상을 설명하는 법칙은?", "o": ["관성의 법칙", "가속도의 법칙", "작용 반작용 법칙", "만유인력의 법칙", "역학적 보존 법칙"]}
    ],
    "운동량과 충격량": [
        {"q": "1. 질량 3kg인 물체가 4m/s의 속도로 달릴 때 이 물체의 운동량의 크기는?", "o": ["3 kg·m/s", "12 kg·m/s", "6 kg·m/s", "24 kg·m/s", "1.33 kg·m/s"]},
        {"q": "2. 충돌 시간이 길어질 때 물체가 받는 평균 충격력의 크기는 어떻게 변하는가?", "o": ["커진다", "일정하다", "작아진다", "예측 불가능하다", "0이 된다"]}
    ],
    "판 구조론과 대륙 이동": [
        {"q": "1. 대륙 이동설을 최초로 주장한 과학자의 이름은?", "o": ["홈스", "헤스", "디츠", "베게너", "로렌츠"]},
        {"q": "2. 맨틀 대류의 상승부에서 판이 갈라지며 새로운 해양 지각이 생성되는 곳은?", "o": ["해구", "해령", "변환 단층", "습곡 산맥", "대륙붕"]}
    ]
}

# 기본 탭 레이아웃 생성
tabs = st.tabs(["01. 단원별 진단 문항 테스트", "02. 메타인지 현황 분석", "03. 한계효용 최적 학습 경로"])

# =========================================================================
# [탭 1] 단원별 진단 문항 테스트 및 실시간 자동 채점
# =========================================================================
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3>01. 단원별 객관식 진단 문항 테스트</h3>", unsafe_allow_html=True)
    
    c_sub, c_big, c_small = st.columns(3)
    sub_sel = c_sub.selectbox("과목 선택", list(st.session_state.db_extended.keys()))
    big_sel = c_big.selectbox("대단원 선택", list(st.session_state.db_extended[sub_sel].keys()))
    
    small_list = [item["소단원"] for item in st.session_state.db_extended[sub_sel][big_sel]]
    small_sel = c_small.selectbox("소단원 선택", small_list)
    
    st.markdown("---")
    
    if small_sel in quiz_bank:
        st.markdown(f"#### 진단 단원: <span class='text-neon'>{sub_sel} [{big_sel} - {small_sel}]</span>", unsafe_allow_html=True)
        
        user_answers = []
        for i, q_data in enumerate(quiz_bank[small_sel]):
            st.markdown(f"<div class='quiz-box'><b>{q_data['q']}</b></div>", unsafe_allow_html=True)
            ans = st.radio("보기 선택", q_data['o'], key=f"quiz_{small_sel}_{i}", horizontal=True)
            user_answers.append(q_data['o'].index(ans) + 1)
            
        # 채점 및 정답 확인 버튼
        if st.button("답안 제출 및 실시간 채점", use_container_width=True):
            target_list = st.session_state.db_extended[sub_sel][big_sel]
            for item in target_list:
                if item["소단원"] == small_sel:
                    correct_ans = item["정답"]
                    score = 0
                    for u_a, c_a in zip(user_answers, correct_ans):
                        if u_a == c_a: score += 50
                    
                    item["실제"] = score
                    item["푼횟수"] += 1
                    st.success(f"채점이 완료되었습니다! 취득 점수: {score}점 / 100점")
            
            with st.expander("정답 및 해설 펼치기"):
                for idx, q_data in enumerate(quiz_bank[small_sel]):
                    correct_idx = [item["정답"] for item in st.session_state.db_extended[sub_sel][big_sel] if item["소단원"] == small_sel][0][idx]
                    st.write(f"**문제 {idx+1} 정답:** {correct_idx}번 | {q_data['o'][correct_idx-1]}")
                    st.caption("해설: 교과 개념에 충실한 문항입니다. 오답 발생 시 3단계 한계효용 처방에 따라 복습을 진행하세요.")
    else:
        st.warning("선택하신 단원의 진단 테스트 문항이 아직 빌드되지 않았습니다. [물리학 I - 뉴턴 운동 법칙] 또는 [지구과학 I - 판 구조론과 대륙 이동] 단원을 선택해 테스트해 보세요!")
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# [탭 2] 메타인지 현황 분석 (학생은 예상 점수만 입력)
# =========================================================================
with tabs[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3>02. 실시간 채점 연동형 메타인지 분석</h3>", unsafe_allow_html=True)
    st.write("1단계에서 채점된 실제 점수가 자동으로 연동됩니다. 학생은 본인이 생각한 **'예상 점수'만 슬라이더로 조절**하세요.")
    
    flat_data = []
    
    with st.form("metacognition_form"):
        for sub, bigs in st.session_state.db_extended.items():
            st.markdown(f"#### {sub}")
            for big, smalls in bigs.items():
                for item in smalls:
                    col_info, col_slider = st.columns([2, 2])
                    with col_info:
                        st.markdown(f"**{big} - {item['소단원']}**")
                        if item["푼횟수"] > 0:
                            st.markdown(f"채점 완료 연동 점수: **{item['실제']}점**")
                        else:
                            st.caption("아직 테스트를 보지 않아 기본값(0점)으로 세팅되어 있습니다.")
                    with col_slider:
                        pred_val = st.slider("내 예상 주관점수", 0, 100, int(item['예상']), key=f"edit_pred_{sub}_{item['소단원']}")
                        item['예상'] = pred_val
                    flat_data.append({"과목": sub, "단원": item['소단원'], "예상": item['예상'], "실제": item['실제'], "시간": item['시간']})
            st.markdown("<div style='border-bottom: 1px dashed #CBD5E1; margin:1rem 0;'></div>", unsafe_allow_html=True)
            
        sync_click = st.form_submit_button("주관적 예상 점수 확정 및 시각화 리포트 생성", use_container_width=True)
        
    df_extended = pd.DataFrame(flat_data)
    df_extended['Gap'] = df_extended['예상'] - df_extended['실제']
    
    def type_classifier(row):
        if abs(row['Gap']) <= 15: return "균형 (메타인지 우수)"
        elif row['Gap'] > 15: return "과대평가 (인지 착각)"
        else: return "과소평가 (실력 숨김)"
    df_extended['유형'] = df_extended.apply(type_classifier, axis=1)
    
    col_t, col_g = st.columns([5, 4])
    with col_t:
        st.markdown("##### 실시간 메타인지 정량 스코어보드")
        st.dataframe(df_extended[['과목', '단원', '예상', '실제', 'Gap', '유형']], use_container_width=True, hide_index=True)
    with col_g:
        st.markdown("##### 종합 4분면 메타인지 매핑 공간")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.set_facecolor('#F8FAFC')
        ax.axhline(50, color='#94A3B8', linestyle='--', alpha=0.5)
        ax.axvline(50, color='#94A3B8', linestyle='--', alpha=0.5)
        ax.plot([0, 100], [0, 100], color='#EF4444', linestyle=':', alpha=0.6, label='Ideal Sync')
        
        for _, row in df_extended.iterrows():
            pt_color = '#6366F1' if row['과목'] == '물리학 I' else '#10B981'
            ax.scatter(row['예상'], row['실제'], color=pt_color, s=150, alpha=0.8, edgecolors='#0F172A')
            ax.text(row['예상']+2, row['실제']+1, row['단원'], fontsize=8)
            
        ax.set_xlim(0, 105)
        ax.set_ylim(0, 105)
        ax.set_xlabel("주관적 예상 점수")
        ax.set_ylabel("자동 채점 실제 점수")
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================================
# [탭 3] 한계효용 기반 최적화 및 내장형 가상 디지털 교과서 구현
# =========================================================================
with tabs[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3>03. 한계효용(MU) 기반 최적 최적화 스케줄링 리포트</h3>", unsafe_allow_html=True)
    
    df_extended['잠재효용'] = 100 - df_extended['실제']
    df_extended['한계효용(MU)'] = df_extended['잠재효용'] / df_extended['시간']
    final_path = df_extended.sort_values(by='한계효용(MU)', ascending=False).reset_index(drop=True)
    
    for idx, row in final_path.iterrows():
        with st.expander(f"우선순위 {idx+1}위 -> {row['과목']} : {row['단원']} (1분 투자당 효율지표: {row['한계효용(MU)']:.2f})"):
            c_desc, c_widget = st.columns([3, 1])
            with c_desc:
                st.markdown(f"**현재 격차 분석:** 1단계 테스트 결과 실제 획득 점수가 **{row['실제']}점**이므로, 공부 시 최대 **{row['잠재효용']}점**의 추가 점수를 즉시 회수할 수 있습니다.")
                st.markdown(f"**시간 효율 소견:** 해당 개념의 EBSi 추천 개념 압축 강의 러닝타임은 총 **{row['시간']}분**으로, 매우 컴팩트하게 구성되어 최적 배정 순위 상위에 랭크되었습니다.")
                
                st.markdown("---")
                st.markdown("##### 06. 정서영의 하이퍼 디지털 온라인 교과서 (가상 빌드 패널)")
                
                textbook_content = ""
                if row['단원'] == "뉴턴 운동 법칙":
                    textbook_content = "■ 제1법칙(관성): 외력이 없으면 정지 물체는 정지, 운동 물체는 등속도 운동 유지.\n■ 제2법칙(가속도): F=ma. 가속도는 힘에 비례하고 질량에 반비례.\n■ 제3법칙(작용 반작용): A가 B에 힘을 가하면, B도 A에 크기가 같고 방향이 반대인 힘을 동시에 가함."
                elif row['단원'] == "운동량과 충격량":
                    textbook_content = "■ 운동량(p): 질량(m) × 속도(v). 방향은 속도의 방향과 일치.\n■ 충격량(I): 힘(F) × 시간(t) = 운동량의 변화량(Delta p).\n■ 충돌 시간을 길게 하면(에어백, 포수 글러브 등) 평균 충격력이 감소하여 파손을 막을 수 있음."
                else:
                    textbook_content = f"■ [{row['단원']}] 핵심 요약 정보:\n본 대단원의 구조적 핵심 원리는 교과 핵심 개념서 제24조에 근거합니다. 해당 개념의 정의와 도식화 데이터를 기반으로 메타인지 오답을 영(0)으로 수렴시키는 공식을 암기하세요."
                
                st.info(textbook_content)
                
            with c_widget:
                st.metric("투입 자원 (시간 비용)", f"{row['시간']} 분")
                st.metric("회수 가치 (기대 효용)", f"+{row['잠재효용']} 점")
                
                st.markdown(f"""
                    <a href="https://www.ebsi.co.kr" target="_blank" style="text-decoration: none;">
                        <div style="
                            width: 100%; 
                            padding: 0.6rem 0; 
                            background-color: #6366F1; 
                            color: white; 
                            border-radius: 8px; 
                            font-weight: 600; 
                            text-align: center;
                            box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
                        ">
                            EBSi 인강 연결
                        </div>
                    </a>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
