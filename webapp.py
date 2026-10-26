import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===================== 全局页面配置 =====================
st.set_page_config(
    page_title="日语专业就业调研数据大屏",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== 全局样式 =====================
st.markdown("""
<style>
    .block-container {padding: 2rem 3rem;}
    .stSidebar {
        background: #0f172a;
        padding-top: 2rem;
    }
    .stSidebar .stButton > button {
        width: 100%;
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 8px;
        background: #1e293b;
        color: #e2e8f0;
        font-size: 15px;
        font-weight: 500;
        text-align: left;
        border: none;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .stSidebar .stButton > button:hover {
        background: #2563eb;
        color: #ffffff;
        font-weight: 700;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .stSidebar .stButton > button:active {
        transform: translateX(2px) scale(0.98);
    }
    .nav-active > button {
        background: #2563eb !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-left: 4px solid #93c5fd !important;
    }
    h1, h2, h3 {color: #0f172a; font-weight: 600;}
    .chart-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
        border: 1px solid #f1f5f9;
    }
    .intro-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 14px;
        padding: 30px 36px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# ===================== 页面状态 =====================
if "current_page" not in st.session_state:
    st.session_state.current_page = "首页"

def switch_page(page_name):
    st.session_state.current_page = page_name

# ===================== 数据读取与工具函数 =====================
@st.cache_data
def load_data():
    df = pd.read_csv("日语就业问卷.csv")
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.replace(["(空)", "", " "], pd.NA)
    # 薪资区间转数值，用于箱型图
    salary_map = {
        "A. 4000及以下": 3000,
        "B. 4000-6000": 5000,
        "C. 6000-8000": 7000,
        "D. 8000以上": 9000
    }
    df["薪资估算值"] = df["22.你的就业薪资区间（应届入职薪资）"].map(salary_map)
    return df

df = load_data()
total = len(df)

def split_multi_ratio(series):
    items = series.dropna().str.split("┋").explode().str.strip()
    count = items.value_counts().reset_index()
    count.columns = ["选项", "人数"]
    count["占比(%)"] = (count["人数"] / total * 100).round(1)
    return count.drop(columns=["人数"])

def col_ratio(series):
    count = series.value_counts().reset_index()
    count.columns = ["选项", "人数"]
    count["占比(%)"] = (count["人数"] / total * 100).round(1)
    return count.drop(columns=["人数"])

hover_style = dict(bgcolor="#0f172a", font_size=13, font_color="white")

# ===================== 侧边栏导航 =====================
with st.sidebar:
    st.markdown("### 📊 调研数据平台")
    st.markdown("---")
    pages = ["首页", "综合数据大屏", "变量交叉分析", "就业预测"]
    for page in pages:
        if st.session_state.current_page == page:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        st.button(page, key=f"nav_{page}", on_click=switch_page, args=(page,))
        if st.session_state.current_page == page:
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("日语专业就业技能专项调研")

# ===================== 页面1：首页 =====================
if st.session_state.current_page == "首页":
    st.markdown("""
    <div class="intro-card">
        <h1 style="margin:0 0 12px 0;">日语专业毕业生就业技能与就业情况专项调研</h1>
        <p style="font-size:16px; color:#334155; line-height:1.7;">
            本调研聚焦日语专业毕业生的就业现状、能力结构与职业发展路径，
            从学历背景、语言证书、实践经历、职场技能、就业去向、薪资水平等多个维度展开系统分析，
            旨在为日语专业在校生的职业规划与能力培养提供数据支撑与现实参考。
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="chart-card">
            <h3>📌 调研维度</h3>
            <ul style="line-height:2; color:#475569;">
                <li>个人背景：毕业年限、最高学历、证书情况</li>
                <li>在校经历：实践深造、职场技能、细分领域知识</li>
                <li>求职就业：择业偏好、对口程度、企业类型、岗位分布</li>
                <li>能力认知：显性竞争力、隐性特质、市场稀缺性</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="chart-card">
            <h3>🧭 平台导航</h3>
            <ul style="line-height:2; color:#475569;">
                <li><b>综合数据大屏</b>：全维度可视化图表，直观呈现整体分布</li>
                <li><b>变量交叉分析</b>：多维度关联分析，挖掘变量间内在联系</li>
            </ul>
            <p style="color:#64748b; font-size:14px; margin-top:12px;">
                所有图表均支持鼠标悬停查看精确数值，部分图表支持缩放、拖拽交互。
            </p>
        </div>
        """, unsafe_allow_html=True)

# ===================== 页面2：综合数据大屏 =====================
elif st.session_state.current_page == "综合数据大屏":
    st.title("📊 综合数据大屏")
    st.caption("全维度分布可视化 · 鼠标悬停查看精确占比")
    st.divider()

    salary_order = ["A. 4000及以下", "B. 4000-6000", "C. 6000-8000", "D. 8000以上"]

    # 第一行：毕业年限环形图 + 学历极坐标玫瑰图
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("毕业年限分布")
        data = col_ratio(df["1.你的毕业年限"])
        fig = px.pie(data, names="选项", values="占比(%)",
                     color_discrete_sequence=px.colors.sequential.Blues_r[1:], hole=0.5)
        fig.update_traces(
            textinfo="label+percent", showlegend=False,
            hoverlabel=hover_style,
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("最高学历分布")
        data = col_ratio(df["2.你的最高学历"])
        fig = go.Figure(go.Barpolar(
            r=data["占比(%)"],
            theta=data["选项"],
            width=[0.6]*len(data),
            marker_color=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb"],
            marker_line_color="white",
            marker_line_width=2,
            hovertemplate="%{theta}<br>占比：%{r}%<extra></extra>",
            hoverlabel=hover_style
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(ticksuffix="%", showline=False)),
            showlegend=False,
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 第二行：日语证书折线图 + 英语证书环形图
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("日语最高等级证书分布")
        data = col_ratio(df["5.你在校期间取得的日语最高等级证书"])
        # 按证书等级排序
        cert_order = ["C. N3及以下", "B. N2", "A. N1", "C. 专业四级", "D. 专业八级", "F. 无等级证书"]
        data = data.set_index("选项").reindex([x for x in cert_order if x in data["选项"].values]).reset_index()
        fig = px.line(data, x="选项", y="占比(%)", markers=True, text="占比(%)",
                      color_discrete_sequence=["#0d9488"])
        fig.update_traces(
            textposition="top center", texttemplate="%{text}%",
            hoverlabel=hover_style,
            marker=dict(size=10, line=dict(width=2, color="white"))
        )
        fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("英语证书持有情况")
        data = col_ratio(df["6.是否持有英语相关证书"])
        fig = px.pie(data, names="选项", values="占比(%)",
                     color_discrete_sequence=px.colors.sequential.Purples_r[1:], hole=0.6)
        fig.update_traces(
            textinfo="label+percent", hoverlabel=hover_style,
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 第三行：就业状态柱状图 + 企业类型矩形树图
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("当前就业状态分布")
        data = col_ratio(df["4.目前就业状态"])
        fig = px.bar(data, x="选项", y="占比(%)", text="占比(%)",
                     color_discrete_sequence=["#2563eb"])
        fig.update_traces(
            texttemplate="%{text}%", textposition="outside",
            hoverlabel=hover_style
        )
        fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white", xaxis_tickangle=-10)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r3c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("入职企业类型分布")
        data = col_ratio(df["20.你目前入职的企业类型"])
        fig = px.treemap(data, path=["选项"], values="占比(%)",
                         color="占比(%)", color_continuous_scale="Teal",
                         range_color=[data["占比(%)"].min()*0.6, data["占比(%)"].max()],
                         hover_data={"占比(%)":":.1f"})
        fig.update_traces(
            texttemplate="%{label}<br>%{value}%",
            hoverlabel=hover_style
        )
        fig.update_layout(coloraxis_showscale=False, margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 第四行：薪资区间面积折线图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("应届入职薪资区间分布")
    data = col_ratio(df["22.你的就业薪资区间（应届入职薪资）"])
    data = data.set_index("选项").reindex(salary_order).reset_index()
    fig = px.area(data, x="选项", y="占比(%)", markers=True, text="占比(%)",
                  color_discrete_sequence=["#2563eb"])
    fig.update_traces(
        textposition="top center", texttemplate="%{text}%",
        hoverlabel=hover_style,
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.15)",
        marker=dict(size=10, line=dict(width=2, color="white"))
    )
    fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 第五行：实践经历横向条形图 + 语言能力雷达图
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("在校日语实践经历占比")
        data = split_multi_ratio(df["3.在校期间是否有日语相关深造/实践经历"])
        data = data.sort_values("占比(%)", ascending=True)
        fig = px.bar(data, y="选项", x="占比(%)", text="占比(%)",
                     orientation="h", color_discrete_sequence=["#ea580c"])
        fig.update_traces(
            texttemplate="%{text}%", textposition="outside",
            hoverlabel=hover_style
        )
        fig.update_layout(xaxis_ticksuffix="%", plot_bgcolor="white", height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r5c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("就业助力最大的语言能力")
        data = split_multi_ratio(df["7.你认为对你就业助力最大的语言能力是（）"])
        fig = go.Figure(data=go.Scatterpolar(
            r=data["占比(%)"], theta=data["选项"],
            fill='toself', line_color="#16a34a",
            fillcolor="rgba(22, 163, 74, 0.25)",
            hoverlabel=hover_style
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, ticksuffix="%")),
            showlegend=False, height=420
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 第六行：显性竞争力雷达图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("显性技能核心竞争力分布")
    data = split_multi_ratio(df["10.求职过程中，你的显性技能核心竞争力是"])
    fig = go.Figure(data=go.Scatterpolar(
        r=data["占比(%)"], theta=data["选项"],
        fill='toself', line_color="#2563eb",
        fillcolor="rgba(37, 99, 235, 0.25)",
        hoverlabel=hover_style
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, ticksuffix="%")),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== 页面3：变量交叉分析 =====================
elif st.session_state.current_page == "变量交叉分析":
    st.title("🔗 变量交叉分析")
    st.caption("选取核心关联维度，挖掘就业特征内在规律")
    st.divider()

    salary_order = ["A. 4000及以下", "B. 4000-6000", "C. 6000-8000", "D. 8000以上"]

    # 1. 学历 × 薪资区间 分组柱状
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("1. 最高学历与薪资区间的关联")
    cross1 = pd.crosstab(df["2.你的最高学历"], df["22.你的就业薪资区间（应届入职薪资）"], normalize="index") * 100
    cross1 = cross1.reindex(columns=salary_order).round(1)
    cross1_long = cross1.reset_index().melt(id_vars="2.你的最高学历", var_name="薪资区间", value_name="占比(%)")
    fig = px.bar(cross1_long, x="2.你的最高学历", y="占比(%)", color="薪资区间",
                 barmode="group", text="占比(%)", color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_traces(texttemplate="%{text}%", textposition="outside", hoverlabel=hover_style)
    fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：横向对比相同学历下不同薪资的占比，直观看出学历层级对薪资上限的影响。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. 日语证书 × 就业状态 热力图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("2. 日语证书等级与就业状态分布")
    cross2 = pd.crosstab(df["5.你在校期间取得的日语最高等级证书"], df["4.目前就业状态"], normalize="columns") * 100
    cross2 = cross2.round(1)
    fig = px.imshow(cross2, text_auto=True, color_continuous_scale="Blues",
                    labels=dict(x="就业状态", y="日语证书等级", color="占比(%)"),
                    zmin=cross2.values.min()*0.5, zmax=cross2.values.max())
    fig.update_layout(coloraxis_colorbar=dict(ticksuffix="%"))
    fig.update_traces(hoverlabel=hover_style)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：颜色越深代表该证书等级在对应就业状态中占比越高，反映证书水平与就业结果的关联程度。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. 实践经历 × 就业目标吻合度 分组柱状图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("3. 实践经历与就业目标吻合度")
    df_temp = df.copy()
    df_temp["有实践经历"] = df_temp["3.在校期间是否有日语相关深造/实践经历"].apply(
        lambda x: "有相关实践" if pd.notna(x) and "无相关经历" not in str(x) else "无相关实践"
    )
    cross3 = pd.crosstab(df_temp["有实践经历"], df_temp["18.你的就业目标与最终就业结果是否一致"], normalize="index") * 100
    cross3 = cross3.round(1)
    cross3_long = cross3.reset_index().melt(id_vars="有实践经历", var_name="目标一致程度", value_name="占比(%)")
    fig = px.bar(cross3_long, x="有实践经历", y="占比(%)", color="目标一致程度",
                 barmode="group", text="占比(%)", color_discrete_sequence=px.colors.sequential.Teal_r)
    fig.update_traces(texttemplate="%{text}%", textposition="outside", hoverlabel=hover_style)
    fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：对比有无实践经历两类人群的就业目标吻合度，体现实践经历对职业规划落地的作用。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. 择业偏好 × 企业类型 热力图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("4. 择业偏好与入职企业类型分布")
    df_pref = df.copy()
    df_pref = df_pref.assign(择业偏好=df_pref["16.在校求职阶段的核心择业偏好"].str.split("┋")).explode("择业偏好")
    df_pref["择业偏好"] = df_pref["择业偏好"].str.strip()
    cross4 = pd.crosstab(df_pref["择业偏好"], df_pref["20.你目前入职的企业类型"], normalize="index") * 100
    cross4 = cross4.round(1)
    fig = px.imshow(cross4, text_auto=True, color_continuous_scale="Purples",
                    labels=dict(x="企业类型", y="择业偏好", color="占比(%)"),
                    zmin=cross4.values.min()*0.5, zmax=cross4.values.max())
    fig.update_layout(coloraxis_colorbar=dict(ticksuffix="%"), height=550)
    fig.update_traces(hoverlabel=hover_style)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：颜色越深代表该择业偏好对应入职企业的占比越高，反映求职预期与实际结果的匹配规律。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. 日语证书等级 × 薪资区间 热力图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("5. 日语证书等级与薪资区间关联")
    cross5 = pd.crosstab(df["5.你在校期间取得的日语最高等级证书"], df["22.你的就业薪资区间（应届入职薪资）"], normalize="index") * 100
    cross5 = cross5.reindex(columns=salary_order).round(1)
    fig = px.imshow(cross5, text_auto=True, color_continuous_scale="Greens",
                    labels=dict(x="薪资区间", y="日语证书等级", color="占比(%)"),
                    zmin=cross5.values.min()*0.5, zmax=cross5.values.max())
    fig.update_layout(coloraxis_colorbar=dict(ticksuffix="%"))
    fig.update_traces(hoverlabel=hover_style)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：对比不同证书等级的薪资分布，体现语言证书对薪资水平的实际影响。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. 求职对口坚持度与最终结果一致性 分组柱状图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("6. 求职对口坚持度与最终结果一致性")
    cross6 = pd.crosstab(df["17.求职初期是否坚持日语专业对口就业"], df["18.你的就业目标与最终就业结果是否一致"], normalize="index") * 100
    cross6 = cross6.round(1)
    cross6_long = cross6.reset_index().melt(id_vars="17.求职初期是否坚持日语专业对口就业", var_name="结果一致程度", value_name="占比(%)")
    fig = px.bar(cross6_long, x="17.求职初期是否坚持日语专业对口就业", y="占比(%)", color="结果一致程度",
                 barmode="group", text="占比(%)", color_discrete_sequence=px.colors.sequential.Oranges_r)
    fig.update_traces(texttemplate="%{text}%", textposition="outside", hoverlabel=hover_style)
    fig.update_layout(yaxis_ticksuffix="%", plot_bgcolor="white", xaxis_title="求职初期对口坚持度")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：对比不同择业坚持度的人群最终目标达成比例，分析坚持专业对口的实际收益。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. 细分领域知识 × 企业类型 热力图
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("7. 日语细分领域知识与入职企业类型")
    df_field = df.copy()
    df_field = df_field.assign(细分领域=df_field["9.是否掌握日语细分领域专业知识"].str.split("┋")).explode("细分领域")
    df_field["细分领域"] = df_field["细分领域"].str.strip()
    cross7 = pd.crosstab(df_field["细分领域"], df_field["20.你目前入职的企业类型"], normalize="columns") * 100
    cross7 = cross7.round(1)
    fig = px.imshow(cross7, text_auto=True, color_continuous_scale="Purples",
                    labels=dict(x="企业类型", y="细分领域知识", color="占比(%)"),
                    zmin=cross7.values.min()*0.5, zmax=cross7.values.max())
    fig.update_layout(coloraxis_colorbar=dict(ticksuffix="%"), height=550)
    fig.update_traces(hoverlabel=hover_style)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：不同细分领域知识对应入职企业的分布差异，体现专项知识对就业方向的导向作用。")
    st.markdown('</div>', unsafe_allow_html=True)

    # 8. 桑基图（修复版）
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("8. 求职路径流向图（坚持度→结果→薪资）")
    # 整理三级链路数据
    sankey_data = df[[
        "17.求职初期是否坚持日语专业对口就业",
        "18.你的就业目标与最终就业结果是否一致",
        "22.你的就业薪资区间（应届入职薪资）"
    ]].dropna()

    # 收集所有节点
    all_nodes = []
    for col in sankey_data.columns:
        for val in sankey_data[col].unique():
            if val not in all_nodes:
                all_nodes.append(val)
    node_index = {name: i for i, name in enumerate(all_nodes)}

    # 生成链接：第一层→第二层
    link1 = sankey_data.groupby([
        "17.求职初期是否坚持日语专业对口就业",
        "18.你的就业目标与最终就业结果是否一致"
    ]).size().reset_index(name="count")
    link1["占比"] = (link1["count"] / len(sankey_data) * 100).round(1)

    # 生成链接：第二层→第三层
    link2 = sankey_data.groupby([
        "18.你的就业目标与最终就业结果是否一致",
        "22.你的就业薪资区间（应届入职薪资）"
    ]).size().reset_index(name="count")
    link2["占比"] = (link2["count"] / len(sankey_data) * 100).round(1)

    # 合并链接
    sources = []
    targets = []
    values = []
    for _, row in link1.iterrows():
        sources.append(node_index[row.iloc[0]])
        targets.append(node_index[row.iloc[1]])
        values.append(row["占比"])
    for _, row in link2.iterrows():
        sources.append(node_index[row.iloc[0]])
        targets.append(node_index[row.iloc[1]])
        values.append(row["占比"])

    # 绘制桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=all_nodes,
            color="#2563eb",
            hoverlabel=hover_style
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(37, 99, 235, 0.4)",
            hoverlabel=hover_style
        )
    )])
    fig.update_layout(height=580, font_size=12)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("解读：完整呈现从求职初期坚持度，到最终目标吻合度，再到薪资区间的完整流向路径，直观展现职业发展链路规律。")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== 页面4：就业预测（独立追加模块，不改动上方任何原有代码） =====================
elif st.session_state.current_page == "就业预测":
    import numpy as np

    st.title("🎯 就业预测")
    st.caption("输入你的基本情况，系统基于历史就业样本为你匹配方向、预测薪资并给出提升建议。")
    st.divider()

    # ---- 隐私说明（小字） ----
    st.markdown(
        '<p style="font-size:12px; color:#64748b; line-height:1.6;">🔒 <b>隐私说明</b>：本页面仅收集学历、证书、实习经历等宽泛的求职相关信息，用于生成就业方向参考，不涉及姓名、联系方式等个人身份信息。你的选择仅用于本次分析，不会被存储，也不会用于其他用途。</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ---- 独立读取量化数据（与原有 load_data 互不影响） ----
    @st.cache_data
    def load_quant_data():
        dfq = pd.read_csv("日语就业量化数据.csv")
        dfq = dfq.dropna(how="all")
        return dfq

    dfq = load_quant_data()

    SALARY_VALUE = {
        "4k以下": 3500, "4-5k": 4500, "5-6k": 5500,
        "6-8k": 7000, "8-10k": 9000, "10-15k": 12500, "15k以上": 16000,
    }
    SALARY_ORDER = list(SALARY_VALUE.keys())
    SALARY_SHORT = ["3.5k", "4.5k", "5.5k", "7k", "9k", "12.5k", "16k"]
    SALARY_LABEL = {
        "4k以下": "月薪 4 千以下", "4-5k": "月薪 4-5 千", "5-6k": "月薪 5-6 千",
        "6-8k": "月薪 6-8 千", "8-10k": "月薪 8-10 千", "10-15k": "月薪 1-1.5 万", "15k以上": "月薪 1.5 万以上",
    }

    EDU_MAP = {"本科": 0, "硕士": 1, "博士": 2}
    CERT_MAP = {"N2以下或无": 0, "N2": 1, "专八": 2, "仅N1": 3, "N1+专八": 4}
    JP_MAP = {"没去过": 0, "短期游学": 1, "3-6个月": 2, "半年以上": 3}
    INTERN_MAP = {"无": 0, "3个月以内": 1, "3-6个月": 2, "6个月以上": 3}
    CITY_MAP = {"二三线": 0, "新一线": 1, "沿海对日城市": 2, "北上广深": 3, "日本": 4}

    FIELD_POOL = ["商务日语", "教育教学", "法律合同", "动漫游戏", "旅游"]
    COMPO_POOL = ["日语+外贸", "日语+运营", "日语+教育", "日语+游戏", "日语+财务"]

    FEAT_WEIGHTS = {
        "日语证书": 0.20, "口语能力": 0.15, "实习时长": 0.15, "日本经历": 0.15,
        "学历": 0.10, "城市选择": 0.10, "复合技能": 0.08, "细分领域": 0.07,
    }

    def encode_df(dfq):
        feats = pd.DataFrame({
            "学历": dfq["学历"].map(EDU_MAP),
            "证书": dfq["日语最高证书"].map(CERT_MAP),
            "口语": pd.to_numeric(dfq["口语自评(1-5)"], errors="coerce").fillna(0),
            "日本经历": dfq["日本经历"].map(JP_MAP),
            "实习": dfq["实习时长"].map(INTERN_MAP),
            "城市": dfq["求职城市"].map(CITY_MAP),
        })
        for p in FIELD_POOL:
            feats["细分_" + p] = dfq["细分领域"].fillna("").str.contains(p).astype(int)
        for p in COMPO_POOL:
            feats["复合_" + p] = dfq["复合技能"].fillna("").str.contains(p).astype(int)
        feats["复合技能数"] = feats[[c for c in feats.columns if c.startswith("复合_")]].sum(axis=1)
        feats["细分领域数"] = feats[[c for c in feats.columns if c.startswith("细分_")]].sum(axis=1)
        return feats

    def encode_user(u):
        feats = pd.Series({
            "学历": EDU_MAP[u["学历"]],
            "证书": CERT_MAP[u["证书"]],
            "口语": u["口语"],
            "日本经历": JP_MAP[u["日本经历"]],
            "实习": INTERN_MAP[u["实习"]],
            "城市": CITY_MAP[u["城市"]],
        })
        for p in FIELD_POOL:
            feats["细分_" + p] = 1 if p in u["细分领域"] else 0
        for p in COMPO_POOL:
            feats["复合_" + p] = 1 if p in u["复合技能"] else 0
        feats["复合技能数"] = sum(1 for c in COMPO_POOL if u["复合技能"].__contains__(c))
        feats["细分领域数"] = sum(1 for c in FIELD_POOL if u["细分领域"].__contains__(c))
        return feats

    def distance(u, row):
        d = 0.0
        w = FEAT_WEIGHTS
        d += w["学历"] * abs(u["学历"] - row["学历"]) / 2
        d += w["日语证书"] * abs(u["证书"] - row["证书"]) / 4
        d += w["口语能力"] * abs(u["口语"] - row["口语"]) / 4
        d += w["日本经历"] * abs(u["日本经历"] - row["日本经历"]) / 3
        d += w["实习时长"] * abs(u["实习"] - row["实习"]) / 3
        d += w["城市选择"] * abs(u["城市"] - row["城市"]) / 4
        field_cols = [c for c in row.index if c.startswith("细分_") and not c.endswith("数")]
        compo_cols = [c for c in row.index if c.startswith("复合_") and not c.endswith("数")]
        for cols, wgt in [(field_cols, w["细分领域"]), (compo_cols, w["复合技能"])]:
            inter = sum(1 for c in cols if u[c] == 1 and row[c] == 1)
            union = sum(1 for c in cols if u[c] == 1 or row[c] == 1)
            if union > 0:
                d += wgt * (1 - inter / union)
        return d

    def pct_of(series, x):
        """百分位：series 中取值 < x 的比例 + 半取 = x 的比例（0-100）"""
        s = series.astype(float)
        below = (s < float(x)).mean()
        equal = (s == float(x)).mean()
        return (below + 0.5 * equal) * 100.0

    feats_all = encode_df(dfq)
    labels_all = dfq["岗位方向"].fillna("未知岗位")
    salaries_all = dfq["薪资区间"].fillna("5-6k")

    DIM_COLS = ["学历", "证书", "口语", "日本经历", "实习", "城市", "复合技能数", "细分领域数"]
    DIM_SHOW = ["学历", "日语证书", "口语能力", "日本经历", "实习时长", "城市选择", "复合技能", "细分领域"]
    DIM_RULES = {
        "日语证书": ("建议冲刺 N1 / 专八——证书是薪资提升最直接的杠杆之一。"),
        "口语能力": ("建议加强口语实战（商务会话、情景表达、模拟面试），口语是面试上岸的关键。"),
        "实习时长": ("建议积累 3-6 个月日语相关实习（外贸、翻译、日企均可），实习是应届就业最大的加分项。"),
        "日本经历": ("有机会争取 3 个月以上的赴日交换/留学/实习，对日企求职有明显加成。"),
        "复合技能": ("可发展「日语+外贸/运营/游戏」等组合，复合型人才在就业市场更稀缺。"),
        "细分领域": ("建议选定一个方向深耕（商务、教育、动漫游戏等），专项知识直接决定岗位方向。"),
        "学历": ("可通过深造，或靠证书、实习的叠加补足竞争力。"),
    }
    SCALE_PER_PCT = 30.0  # 每个百分位点折算的薪资修正（元）

    def predict(u, k=15):
        uf = encode_user(u)
        dists = []
        for i in range(len(feats_all)):
            dists.append((distance(uf, feats_all.iloc[i]), i))
        dists.sort(key=lambda x: x[0])
        top = dists[:k]
        idx = [i for _, i in top]
        sim_salary = salaries_all.iloc[idx]
        sim_job = labels_all.iloc[idx]
        job_freq = sim_job.value_counts(normalize=True).head(3)
        salary_mode = sim_salary.mode().iloc[0]
        sim_mean_base = float(np.mean([SALARY_VALUE[s] for s in sim_salary]))

        # ---- 定制化修正：相似人群基准 + 你相对他们的强弱项微调 ----
        sim_feats = feats_all.iloc[idx]
        delta = 0.0
        user_pct_map = {}
        sim_pct_map = {}
        for col, show in zip(DIM_COLS, DIM_SHOW):
            col_vals = feats_all[col]
            uv = uf[col]
            sv = float(sim_feats[col].mean())
            user_pct_map[show] = pct_of(col_vals, uv)
            sim_pct_map[show] = pct_of(col_vals, sv)
            delta += (user_pct_map[show] - sim_pct_map[show]) * FEAT_WEIGHTS[show] * SCALE_PER_PCT
        salary_est = int(round(sim_mean_base + delta))
        salary_est = max(3000, min(18000, salary_est))

        nearest = min(SALARY_ORDER, key=lambda s: abs(SALARY_VALUE[s] - salary_est))
        overall_mean = float(np.mean([SALARY_VALUE[s] for s in salaries_all]))
        over_pct = (pd.Series([SALARY_VALUE[s] for s in sim_salary]) <= salary_est).mean() * 100
        over_pct_all = (pd.Series([SALARY_VALUE[s] for s in salaries_all]) <= salary_est).mean() * 100

        return {
            "top_idx": idx,
            "job_freq": job_freq,
            "salary_mode": salary_mode,
            "salary_est": salary_est,
            "nearest_label": SALARY_LABEL[nearest],
            "sim_salary": list(sim_salary),
            "sim_mean_base": sim_mean_base,
            "overall_mean": overall_mean,
            "over_pct": over_pct,
            "over_pct_all": over_pct_all,
            "user_pct_map": user_pct_map,
            "sim_pct_map": sim_pct_map,
        }

    # ---- 输入区（问卷星风格，简单直接） ----
    with st.form("predict_form"):
        st.subheader("📝 请填写你的基本情况")
        c1, c2 = st.columns(2)
        with c1:
            edu_in = st.selectbox("最高学历", ["本科", "硕士", "博士"])
            cert_in = st.selectbox("日语最高证书", ["N2以下或无", "N2", "专八", "仅N1", "N1+专八"])
            spoken_in = st.slider("口语自评", 1, 5, 3,
                                  help="5=可商务谈判 · 4=可主持正式场合 · 3=日常沟通流畅 · 2=简单交流 · 1=基本不开口")
            field_in = st.multiselect("掌握的日语细分领域（可多选）", FIELD_POOL)
        with c2:
            jp_in = st.selectbox("日本留学/交换经历", ["没去过", "短期游学", "3-6个月", "半年以上"])
            intern_in = st.selectbox("日语相关实习时长", ["无", "3个月以内", "3-6个月", "6个月以上"])
            city_in = st.selectbox("求职目标城市", ["北上广深", "沿海对日城市", "新一线", "二三线", "日本"])
            compo_in = st.multiselect("复合技能 日语+X（可多选）", COMPO_POOL)
        submitted = st.form_submit_button("🔮 生成我的就业预测", type="primary")

    if submitted:
        u = {
            "学历": edu_in, "证书": cert_in, "口语": spoken_in,
            "日本经历": jp_in, "实习": intern_in, "城市": city_in,
            "细分领域": field_in, "复合技能": compo_in,
        }
        res = predict(u)

        # ========== 输出层1：核心结论 ==========
        st.markdown('<div class="intro-card">', unsafe_allow_html=True)
        top_job = res["job_freq"].index[0]
        top_pct = int(round(res["job_freq"].iloc[0] * 100))
        st.markdown(f"<h2 style='margin:0 0 6px 0;'>✨ 最匹配方向：{top_job}</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='font-size:15px; color:#334155; line-height:1.7;'>你的背景与这一方向的从业者最相似，"
            f"匹配度约 <b>{top_pct}%</b>。结合你相对同类人群的强弱项做微调后，预计月薪约 "
            f"<b>{res['salary_est']/1000:.1f}k</b>（约{res['nearest_label']}）。"
            f"该结果为基于历史样本的统计参考，实际受市场行情、面试表现与岗位供给影响，仅供参考。</p>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ========== 输出层2：备选方向 ==========
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🧭 值得考虑的方向（按匹配度排序）")
        for job, pct in res["job_freq"].items():
            p = int(round(pct * 100))
            st.markdown(
                f"<div style='margin:6px 0;'><span style='font-weight:600; width:150px; display:inline-block;'>{job}</span>"
                f"<div style='display:inline-block; width:45%; height:10px; background:#e2e8f0; border-radius:6px; vertical-align:middle;'>"
                f"<div style='width:{p}%; height:10px; background:linear-gradient(90deg,#2563eb,#60a5fa); border-radius:6px;'></div></div>"
                f"<span style='margin-left:10px; color:#2563eb; font-weight:600;'>{p}%</span></div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ========== 输出层3：四幅差异图 ==========
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📊 你的水平 vs 全体求职者平均水平")
        names1 = DIM_SHOW
        user_r = [round(res["user_pct_map"][n], 1) for n in names1]
        avg_r = [round(res["sim_pct_map"][n], 1) for n in names1]

        # 图1 雷达图（百分位 0-100，各维度统一尺度）
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=user_r + [user_r[0]], theta=names1 + [names1[0]],
            fill="toself", name="你的水平",
            line_color="#2563eb", fillcolor="rgba(37, 99, 235, 0.25)", hoverlabel=hover_style,
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_r + [avg_r[0]], theta=names1 + [names1[0]],
            fill="toself", name="平均水平",
            line_color="#94a3b8", fillcolor="rgba(148, 163, 184, 0.15)", hoverlabel=hover_style,
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True, legend=dict(orientation="h", y=1.08), height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("数值含义：每个维度按「你超过全体求职者的百分比」计算（0-100%），"
                   "不同维度统一到同一尺度，方便横向比较。")

        st.markdown("---")

        # 图2 差异条形图（你的百分位 - 平均百分位，正负分色）
        diff_vals = [round(res["user_pct_map"][n] - res["sim_pct_map"][n], 1) for n in names1]
        colors = ["#2563eb" if v >= 0 else "#f59e0b" for v in diff_vals]
        fig_diff = go.Figure(go.Bar(
            x=diff_vals, y=names1, orientation="h",
            marker_color=colors, text=[f"{v:+.0f}%" for v in diff_vals],
            textposition="outside", hoverlabel=hover_style,
        ))
        fig_diff.add_vline(x=0, line_color="#94a3b8", line_width=1)
        fig_diff.update_layout(
            xaxis_title="相对平均水平（+领先 / -落后）",
            plot_bgcolor="white", height=360, showlegend=False,
        )
        st.plotly_chart(fig_diff, use_container_width=True)

        g1, g2 = st.columns(2)
        with g1:
            # 图3 全体薪资分布：横向条形图（y=薪资档、x=人数），你的档深蓝高亮，条细间距大
            counts_all = salaries_all.value_counts().reindex(SALARY_ORDER).fillna(0).astype(int)
            nearest = min(SALARY_ORDER, key=lambda s: abs(SALARY_VALUE[s] - res["salary_est"]))
            bar_colors = ["#2563eb" if s == nearest else "#93c5fd" for s in SALARY_ORDER]
            fig_hist = go.Figure(go.Bar(
                x=counts_all.values, y=counts_all.index, orientation="h",
                marker_color=bar_colors, width=0.55,
                hoverlabel=hover_style,
            ))
            fig_hist.update_layout(
                title="全体求职者 · 薪资分布",
                xaxis=dict(title="人数", range=[0, int(counts_all.max()) + 8]),
                yaxis_title="月薪区间",
                plot_bgcolor="white", height=400, showlegend=False,
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            if res["over_pct_all"] >= 50:
                _cmp_txt = f"高于统计样本中约 {res['over_pct_all']:.0f}% 的求职者"
            else:
                _cmp_txt = f"低于统计样本中约 {100 - res['over_pct_all']:.0f}% 的求职者"
            st.markdown(
                f"<p style='font-size:16px; font-weight:700; color:#2563eb; margin:-16px 0 2px 0;'>"
                f"📌 你的估算月薪约 {res['salary_est']/1000:.1f}k，{_cmp_txt}</p>",
                unsafe_allow_html=True,
            )
        with g2:
            # 图4 三方对比（估算 ≠ 相似人群均值，体现定制化微调）
            fig_cmp = go.Figure(go.Bar(
                x=["你的估算", "相似人群基准", "全体求职者均值"],
                y=[res["salary_est"], res["sim_mean_base"], res["overall_mean"]],
                marker_color=["#2563eb", "#60a5fa", "#cbd5e1"],
                text=[f"{res['salary_est']/1000:.1f}k", f"{res['sim_mean_base']/1000:.1f}k", f"{res['overall_mean']/1000:.1f}k"],
                textposition="outside", hoverlabel=hover_style,
            ))
            fig_cmp.update_layout(
                title="薪资水平三方对比", yaxis_title="月薪估算（元）",
                plot_bgcolor="white", height=380, showlegend=False,
            )
            st.plotly_chart(fig_cmp, use_container_width=True)
            st.caption("你的估算 = 相似人群基准 + 依据你与该人群强弱差异的微调。")
        st.markdown('</div>', unsafe_allow_html=True)

        # ========== 输出层4：分析与建议（文章式，HTML 加粗，书面措辞） ==========
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🔍 分析与建议")

        strength_dims = [n for n in names1 if n != "城市选择" and res["user_pct_map"][n] >= 60]
        mid_dims = [n for n in names1 if n != "城市选择" and 40 < res["user_pct_map"][n] < 60]
        weak_dims = [n for n in names1 if n != "城市选择" and res["user_pct_map"][n] <= 40]

        def avg_pct(ns):
            return int(round(sum(res["user_pct_map"][n] for n in ns) / len(ns))) if ns else None

        def bdim(ns):
            return "、".join(f"<b>{n}</b>" for n in ns)

        # 整体判断（一段长文）
        para_parts = ["整体来看，"]
        if strength_dims:
            s_val = avg_pct(strength_dims)
            para_parts.append(f"你的竞争力主要来自{bdim(strength_dims)}，综合水平超过统计样本中约 "
                              f"<b>{s_val}%</b> 的求职者，是求职时最扎实的竞争力来源；")
            para_parts.append(f"这意味着在同等条件下，你的起薪起点会高于同届的大多数求职者，"
                              "这一优势在求职初期最容易被雇主直接感知；")
        else:
            para_parts.append("目前尚无特别突出的单项，需要尽快确定一个明确的发力方向；")
        if weak_dims:
            gap = max(50 - avg_pct(weak_dims), 0)
            para_parts.append(f"短板集中在{bdim(weak_dims)}，整体落后样本平均水平约 <b>{gap}%</b>，"
                              "是拉低薪资预期的关键因素，也会在面试中被反复试探；")
        else:
            para_parts.append("各项条件未出现明显短板，整体较为均衡，属于不容易被挑出错漏的类型；")
        if mid_dims:
            para_parts.append(f"{bdim(mid_dims)}处于样本的中等水平，仍有向上提升的空间，"
                              "通常也是拉开差距最容易出效果的环节。")
        para_parts.append("当前阶段，")
        if weak_dims:
            para_parts.append("建议先补齐短板、再强化优势，以提升整体竞争力，"
                              "避免在关键环节被明显短板拖累。")
        else:
            para_parts.append("建议以强化优势、拉开与同水平求职者的差距为主。")
        st.markdown("".join(para_parts), unsafe_allow_html=True)

        st.markdown("---")

        if strength_dims:
            st.markdown(
                f"<b>先说优势。</b>{bdim(strength_dims)}是主要加分项，综合水平超过统计样本中约 "
                f"<b>{avg_pct(strength_dims)}%</b> 的求职者。在样本中同时具备这些条件的求职者占比并不高，"
                "这种稀缺性本身就能带来一定的议价空间。求职与面试环节建议优先展示这些优势，"
                "并把它们作为薪资沟通的主话题，有助于在谈薪时占据主动。",
                unsafe_allow_html=True,
            )
        if weak_dims:
            gap = max(50 - avg_pct(weak_dims), 0)
            st.markdown(
                f"<b>再看短板。</b>{bdim(weak_dims)}整体落后样本平均水平约 <b>{gap}%</b>，"
                "是当前最大的提升空间。短板对薪资的影响往往是整体的：它不一定直接压低起薪，"
                "但会在岗位筛选和定级环节被反复比较。",
                unsafe_allow_html=True,
            )
            st.markdown("建议有针对性地逐项补齐——每补齐一项，薪资预期的上限都会随之抬升。", unsafe_allow_html=True)
            for n in weak_dims:
                st.markdown(f"关于<b>{n}</b>：{DIM_RULES[n]}", unsafe_allow_html=True)
        if mid_dims:
            st.markdown(
                f"<b>保持观察。</b>{bdim(mid_dims)}目前处于样本中等水平，未构成明显短板，仍有提升空间。"
                "这类项目往往决定你与同水平求职者最终拉开差距的幅度，值得持续投入、不宜过早放弃。",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.caption("以上分析基于我们统计的历史样本规律生成，供职业规划参考，不构成求职承诺。")
        st.markdown('</div>', unsafe_allow_html=True)

