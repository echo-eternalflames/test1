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
    pages = ["首页", "综合数据大屏", "变量交叉分析"]
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
