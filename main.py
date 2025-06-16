import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

st.set_page_config(
    page_title="Player Analytics",
    page_icon="media/favicon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)
# Load the data
df = pd.read_csv("data_for_streamlit.csv")
st.sidebar.image("media/cricket-logo.png", use_container_width= True)
# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard","Score Predictor","Interactive Data Table", "About" ])
for _ in range(18):
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Footer content
st.sidebar.markdown("---")
st.sidebar.markdown("Dhanush Devadiga")
if page == "About":
    st.title("About")
    col1, col2 = st.columns(2)
    with col1:
        st.image("media/virat-kohli.png", caption="Virat Kohli - Indian Cricketer", use_container_width=True)

    with col2:
        st.write("## Virat Kohli")
        st.write("""
Virat Kohli is one of the most celebrated cricketers of the modern era.
Born on November 5, 1988, in Delhi, India, he made his international debut in 2008.
He quickly became known for his consistency, passion, and hunger to win.

**Batting style & strengths**            
As a batsman, he blends classical technique with fearless stroke play.
Kohli has represented India in all three formats i.e Tests, ODIs, and T20Is.

**Career highlights**
- Former Captain of the Indian national team across all formats
- ICC Cricketer of the Decade (2010–2020)
- 80+ international centuries across formats
- 25,000+ international runs to his name
- Revolutionized fitness standards in Indian cricket
- Known as the "Chase Master" for his success in run-chases

**Leadership & impact**            
    Under his captaincy, India won a historic Test series in Australia.
    He took India to the top of the ICC Test rankings with a bold, aggressive style.
    Kohli emphasized team culture, accountability, and relentless effort.

**Beyond cricket**            
    He is a global icon, philanthropist, and entrepreneur.
    Kohli supports causes like animal welfare, fitness, and child education.
    His journey inspires millions to chase excellence and stay true to their passion.

**A legacy in motion**            
    Kohli continues to lead with pride, heart, and an unbreakable will to win.
        """)
elif page == "Score Predictor":
    st.title("Cricket Score Predictor")

    match_types = df['Match Type'].dropna().unique()
    selected_match_type = st.selectbox("Select Match Type", match_types)

    filtered_df = df[df['Match Type'] == selected_match_type]

    if not filtered_df.empty:
        oppositions = filtered_df['Opposition'].dropna().unique()
        selected_opposition = st.selectbox("Select Opposition", oppositions)

        filtered_df = filtered_df[filtered_df['Opposition'] == selected_opposition]

        if not filtered_df.empty:
            grounds = filtered_df['Ground'].dropna().unique()
            selected_ground = st.selectbox("Select Ground", grounds)

            final_df = filtered_df[filtered_df['Ground'] == selected_ground]

            if st.button("🔮 Predict Score"):
                if final_df.empty:
                    st.error("No records found for this combination. Unable to generate score prediction.")
                else:
                    with st.spinner("Calculating score prediction..."):
                        time.sleep(2)
                        predicted_score = round(final_df['Runs'].mean())
                    st.success(f"Predicted Score: {predicted_score}")
        else:
            st.error("No grounds found for this opposition in selected match type.")
    else:
        st.error("No data found for selected Match Type.")
elif page == "Interactive Data Table":


    df['Start Date'] = pd.to_datetime(df['Start Date'])

    # Unique keys to avoid clashing with other session state
    match_type_key = "interactive_match_type"
    sort_order_key = "interactive_sort_order"
    selected_oppositions_key = "interactive_selected_oppositions"
    year_range_key = "interactive_year_range"

    # Set up session state for this page
    if match_type_key not in st.session_state:
        st.session_state[match_type_key] = "All"
    if sort_order_key not in st.session_state:
        st.session_state[sort_order_key] = "Newest First"
    if selected_oppositions_key not in st.session_state:
        st.session_state[selected_oppositions_key] = []
    if year_range_key not in st.session_state:
        st.session_state[year_range_key] = (int(df['Year'].min()), int(df['Year'].max()))

    st.title("Match Records Viewer")

    with st.expander("**Configuration**", icon="⚙"):
        row1 = st.columns(3)

        with row1[0]:
            match_types = df['Match Type'].dropna().unique().tolist()
            st.session_state[match_type_key] = st.selectbox(
                "Filter by Match Type:",
                ["All"] + sorted(match_types),
                index=(["All"] + sorted(match_types)).index(st.session_state[match_type_key])
            )

        with row1[1]:
            st.session_state[sort_order_key] = st.selectbox(
                "Sort by Start Date:",
                ["Newest First", "Oldest First"],
                index=["Newest First", "Oldest First"].index(st.session_state[sort_order_key])
            )

        with row1[2]:
            opposition_values = df['Opposition'].dropna().unique().tolist()
            st.session_state[selected_oppositions_key] = st.multiselect(
                "Filter by Opposition:",
                sorted(opposition_values),
                default=st.session_state[selected_oppositions_key]
            )

        min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
        st.session_state[year_range_key] = st.slider(
            "Filter by Year Range:",
            min_value=min_year,
            max_value=max_year,
            value=st.session_state[year_range_key]
        )

    # Apply filters
    filtered_df = df.copy()

    if st.session_state[match_type_key] != "All":
        filtered_df = filtered_df[filtered_df['Match Type'] == st.session_state[match_type_key]]

    if st.session_state[selected_oppositions_key]:
        filtered_df = filtered_df[filtered_df['Opposition'].isin(st.session_state[selected_oppositions_key])]

    filtered_df = filtered_df[
        filtered_df['Year'].between(
            st.session_state[year_range_key][0], st.session_state[year_range_key][1]
        )
    ]

    filtered_df = filtered_df.sort_values(
        "Start Date", ascending=(st.session_state[sort_order_key] == "Oldest First")
    )

    filtered_df['Start Date'] = filtered_df['Start Date'].dt.strftime('%Y-%m-%d')

    # Optional columns to hide
    columns_to_hide = ['Inns', 'Year', 'MOM_Won', 'Pos']
    display_df = filtered_df.reset_index(drop=True)
    display_df = display_df.drop(columns=[col for col in columns_to_hide if col in display_df.columns])

    st.dataframe(display_df, use_container_width=True)

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_matches.csv",
        mime="text/csv"
    )


else:
# Inject sticky header
    st.markdown("""
        <style>
        .sticky-title {
            position: fixed;
            top: 0;
            right: 0;
            width: 98%;
            background-color: #0E1117;
            z-index: 99999;
            padding: 0.5rem;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            border-bottom: 2px solid #3488BD;
        }

        /* Push the main app content down */
        .main {
            margin-top: 99px;
        }
        </style>
        <div class="sticky-title"> Player Analytics Dashboard</div>
    """, unsafe_allow_html=True)



    # Tabs: Add "Overall" tab first, followed by match types
    match_types = df["Match Type"].unique().tolist()
    tab_labels = ["Overall"] + match_types
    tabs = st.tabs(tab_labels)

    for match_type, tab in zip(tab_labels, tabs):
        with tab:
            if match_type == "Overall":
                match_df = df
            else:
                match_df = df[df["Match Type"] == match_type]

            # Metrics display
            total_runs = match_df["Runs"].sum()
            total_matches = match_df.shape[0]
            avg_strike_rate = match_df["SR"].mean()
            best_score = match_df["Runs"].max()
            num_hundreds = match_df[match_df["Runs"] >= 100].shape[0]
            num_fifties = match_df[(match_df["Runs"] >= 50) & (match_df["Runs"] < 100)].shape[0]
            st.markdown("""
            <style>
            /* Apply box shadow and border radius to each column */
            div[data-testid="stHorizontalBlock"] > div {
                box-shadow: 2px 2px 6px #3488BD;
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 0.5rem;
                background-color: #0E1117;
            }

            /* Style the metric value */
            div[data-testid="stMetricValue"] {
                font-size: 1.4em;
                font-weight: 700;
                color: #3488BD;
                padding-top: 0.2rem;
                padding-bottom: 0.7rem;
            }
            </style>
            """, unsafe_allow_html=True)
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("Total Runs", f"{total_runs}")
            col2.metric("Matches Played", f"{total_matches}")
            col3.metric("Avg. Strike Rate", f"{avg_strike_rate:.2f}")
            col4.metric("Best Score", f"{best_score}")
            col5.metric("No. of 100s", f"{num_hundreds}")
            col6.metric("No. of 50s", f"{num_fifties}")

            # Row 1
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                st.subheader("Runs Scored vs Year")
                with st.expander("**Configuration**", icon="⚙"):
                    min_year, max_year = df['Year'].min(), df['Year'].max()
                    year_range = st.slider(
                        "Select Year Range",
                        min_value=min_year,
                        max_value=max_year,
                        value=(min_year, max_year),
                        key=f"year_slider_{match_type}"
                    )

                filtered_df = df if match_type == "Overall" else df[df["Match Type"] == match_type]
                filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

                grouped_df = filtered_df.groupby(['Year', 'Match Type'])['Runs'].sum().reset_index()
                fig = px.area(
                    grouped_df,
                    x='Year',
                    y='Runs',
                    color='Match Type',
                    title=' ',
                    labels={'Runs': 'Total Runs', 'Year': 'Year'},
                    template='plotly_white',
                    color_discrete_sequence=px.colors.sequential.Blues[::-3]
                )
                fig.update_layout(
                    title_font_size=22,
                    xaxis_title_font_size=16,
                    yaxis_title_font_size=16,
                    legend_title_text='Match Type',
                    margin=dict(l=40, r=40, t=60, b=40)
                )
                fig.update_traces(mode='lines', hovertemplate='Year: %{x}<br>Runs: %{y}<br>Type: %{legendgroup}')
                st.plotly_chart(fig, use_container_width=True, key=f"area_chart_{match_type}")

            with row1_col2:
                st.subheader("Matches Played Against Countries")
                country_counts = match_df['Opposition'].value_counts().reset_index()
                country_counts.columns = ['Country', 'Matches']

                with st.expander("**Configuration**", icon="⚙"):
                    top_n = st.slider("Number of Countries", 3, len(country_counts), 6, key=f"slider_{match_type}")

                top_countries = country_counts.head(top_n)

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=top_countries['Matches'],
                    theta=top_countries['Country'],
                    fill='toself',
                    name='Matches Played',
                    line_color='rgba(70, 130, 180, 0.85)',
                    fillcolor='rgba(70, 130, 180, 0.3)',
                    hovertemplate='<b>%{theta}</b><br>Matches: %{r}<extra></extra>'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, showticklabels=True, showline=False, gridcolor='#B8B8C3'),
                        angularaxis=dict(gridcolor='#B8B8C3'),
                        bgcolor='#0E1117'
                    ),
                    title=" ",
                    font=dict(family='Arial', size=14),
                    showlegend=False,
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    margin=dict(l=30, r=30, t=70, b=30)
                )
                st.plotly_chart(fig, use_container_width=True)

            # Row 2
            row2_col1, row2_col2 = st.columns(2)
            with row2_col1:
                st.subheader("Top 5 Scoring Grounds")
                filtered_df = df if match_type == "Overall" else df[df["Match Type"] == match_type]
                ground_group = filtered_df.groupby(['Ground', 'Match Type'])['Runs'].sum().reset_index()
                top_5_grounds = ground_group.groupby('Ground')['Runs'].sum().nlargest(5).index
                top_grounds_df = ground_group[ground_group['Ground'].isin(top_5_grounds)]

                fig = px.bar(
                    top_grounds_df,
                    x='Runs',
                    y='Ground',
                    color='Match Type',
                    orientation='h',
                    text='Runs',
                    color_discrete_sequence=px.colors.sequential.Blues[::-3]
                )
                fig.update_layout(
                    yaxis=dict(categoryorder='total ascending'),
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(size=13),
                    margin=dict(l=60, r=30, t=60, b=30)
                )
                fig.update_traces(textposition='inside')
                st.plotly_chart(fig, use_container_width=True, key=f"grounds_chart_{match_type}")

            with row2_col2:
                st.subheader("Runs by Batting Position")
                filtered_df = df if match_type == "Overall" else df[df["Match Type"] == match_type]
                filtered_df['Pos'] = filtered_df['Pos'].astype(str)
                position_runs = filtered_df.groupby('Pos')['Runs'].sum().reset_index().sort_values(by='Runs', ascending=False)

                fig = px.bar(
                    position_runs,
                    x='Pos',
                    y='Runs',
                    text='Runs',
                    color='Runs',
                    color_continuous_scale=px.colors.sequential.Blues
                )
                fig.update_layout(
                    xaxis_title="Batting Position",
                    yaxis_title="Total Runs",
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(size=13),
                    margin=dict(l=40, r=30, t=60, b=60),
                    coloraxis_showscale=False
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True, key=f"batting_pos_chart_{match_type}")

            # Row 3
            row3 = st.columns(1)
            with row3[0]:
                st.subheader("Total Runs Over the Years")
                st.markdown("Explore the total runs scored over the years and analyze the trends.")

                with st.expander("**Configuration**", icon="\u2699"):
                    min_year = df['Year'].min()
                    max_year = df['Year'].max()
                    year_range = st.slider(
                        "Select Year Range",
                        min_value=min_year,
                        max_value=max_year,
                        value=(min_year, max_year),
                        step=1,
                        key=f"year_slider_row3_{match_type}"
                    )

                filtered_df = df if match_type == "Overall" else df[df['Match Type'] == match_type]
                filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]
                yearly_runs = filtered_df.groupby('Year')['Runs'].sum().reset_index()

                start_year, end_year = year_range
                if start_year in yearly_runs['Year'].values and end_year in yearly_runs['Year'].values:
                    start_runs = yearly_runs[yearly_runs['Year'] == start_year]['Runs'].values[0]
                    end_runs = yearly_runs[yearly_runs['Year'] == end_year]['Runs'].values[0]
                    if start_runs > 0:
                        pct_change = ((end_runs - start_runs) / start_runs) * 100
                        pct_text = f"{abs(pct_change):.2f}%"
                        if pct_change > 0:
                            trend_msg = f"The runs have <strong>increased</strong> by <span style='color:green;'>▲ {pct_text}</span> from <strong>{start_year}</strong> to <strong>{end_year}</strong>."
                        else:
                            trend_msg = f"The runs have <strong>decreased</strong> by <span style='color:red;'>▼ {pct_text}</span> from <strong>{start_year}</strong> to <strong>{end_year}</strong>."
                    else:
                        trend_msg = "Cannot calculate trend due to zero runs in the start year."
                else:
                    trend_msg = "Data not available for one or both selected years."

                fig = px.line(
                    yearly_runs,
                    x='Year',
                    y='Runs',
                    markers=True,
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                fig.update_layout(
                    xaxis_title='Year',
                    yaxis_title='Total Runs',
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(size=13),
                    margin=dict(l=60, r=30, t=60, b=30),
                    xaxis=dict(tickmode='linear', tick0=min_year, dtick=1)
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=6))

                st.markdown("### Trend Analysis")
                st.markdown(trend_msg, unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, key=f"row3_runs_chart_{match_type}")
custom_css = """
<style>
.st-emotion-cache-kgpedg {
    display: flex;
    justify-content: space-around !important;
    align-items: center !important;
    padding: 0;
}
.st-emotion-cache-luriig {
    position: fixed;
    top: 0px;
    left: 0px;
    right: 0px;
    height: 0.75rem;
    background: rgb(14, 17, 23);
    outline: none;
    z-index: 999990;
    display: block;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)