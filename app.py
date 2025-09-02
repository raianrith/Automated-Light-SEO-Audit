import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
from datetime import datetime
import io

# Configure page
st.set_page_config(
    page_title="SEO Performance Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 5px;
        border-left: 4px solid #3498db;
    }
    
    .instruction-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .insight-box {
        background-color: #f8fff8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .file-upload-section {
        background-color: #fafafa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #ccc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<div class="main-header">🚀 SEO Performance Analyzer</div>', unsafe_allow_html=True)
    
    # Sidebar guide
    with st.sidebar:
        st.markdown("### 📚 How It Works")
        st.markdown("""
        1. **Choose** an analysis tab above
        2. **Upload** required CSV/Excel files  
        3. **Review** automated insights
        4. **Download** your reports
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔧 Data Sources")
        st.markdown("""
        - **Semrush**: Keyword rankings & competition data
        - **Google Search Console**: Click & impression metrics
        - **GA4**: Traffic & conversion analytics
        """)
        
        st.markdown("---")
        
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        - Export in **CSV or Excel format** (never PDF)
        - Use **consistent date ranges** across all exports
        - **Same month comparisons** for YoY analysis
        - Check column headers match expectations
        """)
    
    # Enhanced tab navigation with more sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📋 Data Export Guide",
        "📊 Visibility Trends", 
        "🔄 Keyword Movement", 
        "📄 Page Performance",
        "🎯 Query Analysis",
        "🏁 Competitor Gaps",
        "📈 Traffic Attribution", 
        "🚧 More Soon"
    ])
    
    with tab1:
        data_export_instructions()
        
    with tab2:
        keyword_visibility_analysis()
        
    with tab3:
        keyword_movement_analysis()
        
    with tab4:
        page_performance_analysis()
        
    with tab5:
        query_gains_losses_analysis()
        
    with tab6:
        competitor_analysis()
        
    with tab7:
        traffic_attribution_analysis()
        
    with tab8:
        st.markdown("""
        ### 🚀 Future Analysis Modules:
        
        **🤖 SERP Features Impact**
        - AI Overviews presence & inclusion rates
        - Featured snippets analysis
        - SERP feature CTR impact
        
        **🔧 Technical SEO Health** 
        - Core Web Vitals tracking
        - Crawl error analysis
        - Index coverage insights
        
        **📱 Mobile Performance**
        - Mobile vs desktop rankings
        - Mobile usability issues
        - AMP performance analysis
        
        **🌍 Local SEO Analysis**
        - Local pack rankings
        - GMB performance metrics
        - Local citation analysis
        
        *Each module will include interactive charts, automated insights, and actionable recommendations!*
        """)
        
        st.markdown("---")
        st.markdown("**💬 Have specific analysis needs? The framework is designed to be extensible!**")

# Helper functions for file processing
def read_uploaded_file(uploaded_file):
    """Read uploaded CSV or Excel file"""
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            return pd.read_excel(uploaded_file)
        else:
            return pd.read_csv(uploaded_file)
    return None

def normalize_columns(df):
    """Normalize column names by cleaning whitespace and special characters"""
    df = df.copy()
    df.columns = [re.sub(r"\s+", " ", str(c).replace("\xa0", " ")).strip() for c in df.columns]
    return df

def find_column(columns, patterns):
    """Find column by searching for patterns (case-insensitive)"""
    columns_lower = {str(c).lower(): c for c in columns}
    for pattern in patterns:
        pattern_lower = pattern.lower()
        for col_lower, original_col in columns_lower.items():
            if pattern_lower in col_lower:
                return original_col
    return None

def keyword_visibility_analysis():
    st.markdown('<div class="section-header">🔍 Keyword Visibility Trends (Year-over-Year)</div>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis compares your keyword rankings between two time periods (typically current year vs last year) to understand:</p>
        <ul>
            <li><b>Total keyword footprint changes</b> - Are you ranking for more or fewer keywords?</li>
            <li><b>Ranking quality distribution</b> - What percentage of keywords are in top positions?</li>
            <li><b>Strategic insights</b> - Whether you're gaining authority or losing visibility breadth</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>2 Semrush Positions CSV files</b>:</p>
        <ol>
            <li><b>Current Period:</b> Recent Semrush Positions export (current month)</li>
            <li><b>Previous Period:</b> Same month from previous year (for YoY comparison)</li>
        </ol>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Total keywords change (Δ and %)</li>
            <li>Ranking distribution by position buckets</li>
            <li>Quality vs quantity analysis</li>
            <li>Strategic recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="file-upload-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Current Period (2024/2025)")
        current_file = st.file_uploader(
            "Upload current Semrush Positions file",
            type=['csv', 'xlsx', 'xls'],
            key="current_positions",
            help="Export from Semrush: Domain Analytics → Organic Research → Positions (CSV or Excel format)"
        )
        
    with col2:
        st.markdown("#### 📤 Previous Period (Same Month Last Year)")
        previous_file = st.file_uploader(
            "Upload previous year Semrush Positions file", 
            type=['csv', 'xlsx', 'xls'],
            key="previous_positions",
            help="Same export but for the corresponding month last year (CSV or Excel format)"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process files if both are uploaded
    if current_file is not None and previous_file is not None:
        # Add Run Analysis button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Run Visibility Analysis", key="run_visibility", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing your data..."):
                    try:
                        # Load data using helper functions
                        current_df = normalize_columns(read_uploaded_file(current_file))
                        previous_df = normalize_columns(read_uploaded_file(previous_file))
                        
                        # Validate data
                        validation_passed, validation_message = validate_positions_data(current_df, previous_df)
                        
                        if not validation_passed:
                            st.markdown(f'<div class="warning-box">{validation_message}</div>', unsafe_allow_html=True)
                            return
                        
                        # Perform analysis
                        analysis_results = analyze_keyword_visibility(current_df, previous_df)
                        
                        # Display results
                        display_visibility_results(analysis_results)
                        
                    except Exception as e:
                        st.error(f"❌ Error processing files: {str(e)}")
                        st.info("💡 Please ensure you've uploaded valid Semrush Positions CSV or Excel files")
    else:
        if current_file is None:
            st.info("📤 Please upload the current period Semrush Positions file")
        if previous_file is None:
            st.info("📤 Please upload the previous period Semrush Positions file")

def validate_positions_data(current_df, previous_df):
    """Validate the uploaded Semrush positions data"""
    required_columns = ['Keyword', 'Position']
    
    # Check if required columns exist
    for df, period in [(current_df, 'current'), (previous_df, 'previous')]:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"❌ Missing required columns in {period} file: {missing_columns}. Available columns: {list(df.columns)}"
    
    # Check if data is not empty
    if len(current_df) == 0 or len(previous_df) == 0:
        return False, "❌ One or both files appear to be empty"
    
    # Check for valid position data
    for df, period in [(current_df, 'current'), (previous_df, 'previous')]:
        if df['Position'].isna().all():
            return False, f"❌ No valid position data found in {period} file"
    
    return True, "✅ Data validation passed"

def analyze_keyword_visibility(current_df, previous_df):
    """Analyze keyword visibility trends"""
    
    # Clean position data - convert to numeric, handle non-numeric values
    def clean_positions(df):
        df = df.copy()
        df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
        df = df.dropna(subset=['Position'])
        return df
    
    current_clean = clean_positions(current_df)
    previous_clean = clean_positions(previous_df)
    
    # Calculate total keywords
    total_current = len(current_clean)
    total_previous = len(previous_clean)
    
    # Calculate rank buckets
    def get_rank_buckets(df):
        return {
            'top_3': len(df[df['Position'] <= 3]),
            'top_4_10': len(df[(df['Position'] > 3) & (df['Position'] <= 10)]),
            'top_11_20': len(df[(df['Position'] > 10) & (df['Position'] <= 20)]),
            'top_21_plus': len(df[df['Position'] > 20])
        }
    
    current_buckets = get_rank_buckets(current_clean)
    previous_buckets = get_rank_buckets(previous_clean)
    
    # Calculate changes
    total_change = total_current - total_previous
    total_change_pct = (total_change / total_previous * 100) if total_previous > 0 else 0
    
    # Calculate bucket changes
    bucket_changes = {}
    for bucket in current_buckets:
        current_count = current_buckets[bucket]
        previous_count = previous_buckets[bucket]
        change = current_count - previous_count
        change_pct = (change / previous_count * 100) if previous_count > 0 else 0
        
        bucket_changes[bucket] = {
            'current': current_count,
            'previous': previous_count,
            'change': change,
            'change_pct': change_pct,
            'current_share': (current_count / total_current * 100) if total_current > 0 else 0,
            'previous_share': (previous_count / total_previous * 100) if total_previous > 0 else 0
        }
    
    return {
        'total_current': total_current,
        'total_previous': total_previous,
        'total_change': total_change,
        'total_change_pct': total_change_pct,
        'bucket_changes': bucket_changes,
        'current_df': current_clean,
        'previous_df': previous_clean
    }

def display_visibility_results(results):
    """Display the keyword visibility analysis results"""
    
    # Key metrics section
    st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if results['total_change'] >= 0 else "inverse"
        st.metric(
            label="Total Keywords",
            value=f"{results['total_current']:,}",
            delta=f"{results['total_change']:,} ({results['total_change_pct']:.1f}%)",
            delta_color=delta_color
        )
    
    with col2:
        top_3_current = results['bucket_changes']['top_3']['current_share']
        top_3_previous = results['bucket_changes']['top_3']['previous_share']
        top_3_delta = top_3_current - top_3_previous
        st.metric(
            label="Top 3 Rankings",
            value=f"{top_3_current:.1f}%",
            delta=f"{top_3_delta:+.1f}%"
        )
    
    with col3:
        top_10_current = results['bucket_changes']['top_3']['current_share'] + results['bucket_changes']['top_4_10']['current_share']
        top_10_previous = results['bucket_changes']['top_3']['previous_share'] + results['bucket_changes']['top_4_10']['previous_share']
        top_10_delta = top_10_current - top_10_previous
        st.metric(
            label="Top 10 Rankings",
            value=f"{top_10_current:.1f}%",
            delta=f"{top_10_delta:+.1f}%"
        )
    
    with col4:
        # Quality score (weighted average of rankings)
        def calc_quality_score(buckets, total):
            if total == 0:
                return 0
            score = ((buckets['top_3'] * 100) + 
                    (buckets['top_4_10'] * 75) + 
                    (buckets['top_11_20'] * 50) + 
                    (buckets['top_21_plus'] * 25)) / total
            return score
        
        current_quality = calc_quality_score(
            {k: v['current'] for k, v in results['bucket_changes'].items()}, 
            results['total_current']
        )
        previous_quality = calc_quality_score(
            {k: v['previous'] for k, v in results['bucket_changes'].items()}, 
            results['total_previous']
        )
        quality_delta = current_quality - previous_quality
        
        st.metric(
            label="Quality Score",
            value=f"{current_quality:.1f}",
            delta=f"{quality_delta:+.1f}",
            help="Weighted score: Top 3=100pts, 4-10=75pts, 11-20=50pts, 21+=25pts"
        )
    
    # Visualization section
    st.markdown('<div class="section-header">📊 Ranking Distribution Analysis</div>', unsafe_allow_html=True)
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Ranking distribution comparison chart
        bucket_labels = ['Top 3', '4-10', '11-20', '21+']
        current_values = [results['bucket_changes'][k]['current'] for k in ['top_3', 'top_4_10', 'top_11_20', 'top_21_plus']]
        previous_values = [results['bucket_changes'][k]['previous'] for k in ['top_3', 'top_4_10', 'top_11_20', 'top_21_plus']]
        
        fig_distribution = go.Figure(data=[
            go.Bar(name='Previous Period', x=bucket_labels, y=previous_values, marker_color='lightblue'),
            go.Bar(name='Current Period', x=bucket_labels, y=current_values, marker_color='darkblue')
        ])
        
        fig_distribution.update_layout(
            title='Keyword Count by Ranking Position',
            xaxis_title='Ranking Position',
            yaxis_title='Number of Keywords',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_distribution, use_container_width=True)
    
    with viz_col2:
        # Share distribution pie charts
        fig_pie = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type':'domain'}, {'type':'domain'}]],
            subplot_titles=('Previous Period', 'Current Period')
        )
        
        # Previous period pie
        fig_pie.add_trace(go.Pie(
            labels=bucket_labels,
            values=previous_values,
            name="Previous",
            marker_colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ), 1, 1)
        
        # Current period pie
        fig_pie.add_trace(go.Pie(
            labels=bucket_labels,
            values=current_values,
            name="Current",
            marker_colors=['#ff6666', '#3399ff', '#66ff66', '#ffb366']
        ), 1, 2)
        
        fig_pie.update_layout(
            title_text="Ranking Distribution Share",
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed changes table
    st.markdown('<div class="section-header">📋 Detailed Changes by Ranking Bucket</div>', unsafe_allow_html=True)
    
    # Create detailed table
    table_data = []
    bucket_map = {
        'top_3': 'Top 3 (1-3)',
        'top_4_10': '4-10',
        'top_11_20': '11-20',
        'top_21_plus': '21+'
    }
    
    for bucket_key, bucket_name in bucket_map.items():
        data = results['bucket_changes'][bucket_key]
        table_data.append({
            'Ranking Position': bucket_name,
            'Previous Count': data['previous'],
            'Current Count': data['current'],
            'Change': data['change'],
            'Change %': f"{data['change_pct']:.1f}%",
            'Previous Share': f"{data['previous_share']:.1f}%",
            'Current Share': f"{data['current_share']:.1f}%"
        })
    
    table_df = pd.DataFrame(table_data)
    st.dataframe(table_df, use_container_width=True)
    
    # Strategic insights
    st.markdown('<div class="section-header">💡 Strategic Insights & Interpretation</div>', unsafe_allow_html=True)
    
    insights = generate_visibility_insights(results)
    st.markdown(f'<div class="insight-box">{insights}</div>', unsafe_allow_html=True)
    
    # Download section
    st.markdown('<div class="section-header">📥 Download Results</div>', unsafe_allow_html=True)
    
    # Create summary report
    summary_report = create_visibility_summary_report(results)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Download Summary Report",
            data=summary_report,
            file_name=f"keyword_visibility_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col2:
        # Convert table to CSV for download
        csv_buffer = io.StringIO()
        table_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📊 Download Data Table (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"keyword_visibility_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def generate_visibility_insights(results):
    """Generate strategic insights based on the visibility analysis"""
    
    total_change = results['total_change']
    total_change_pct = results['total_change_pct']
    
    top_3_change = results['bucket_changes']['top_3']['change_pct']
    top_10_current_share = (results['bucket_changes']['top_3']['current_share'] + 
                           results['bucket_changes']['top_4_10']['current_share'])
    top_10_previous_share = (results['bucket_changes']['top_3']['previous_share'] + 
                            results['bucket_changes']['top_4_10']['previous_share'])
    
    insights = []
    
    # Overall trend analysis
    if total_change > 0:
        insights.append(f"<b>🟢 Keyword Footprint Growth:</b> You're ranking for {abs(total_change):,} more keywords ({total_change_pct:+.1f}%), indicating expanding organic visibility.")
    elif total_change < 0:
        insights.append(f"<b>🟡 Keyword Footprint Decline:</b> You've lost rankings for {abs(total_change):,} keywords ({total_change_pct:.1f}%), but this could signal a focus on quality over quantity.")
    else:
        insights.append("<b>🟨 Stable Keyword Count:</b> Your total keyword footprint remained stable year-over-year.")
    
    # Quality analysis
    if top_3_change > 10:
        insights.append(f"<b>🟢 Strong Authority Growth:</b> Top 3 rankings increased by {top_3_change:.1f}%, showing significant improvement in search authority.")
    elif top_3_change > 0:
        insights.append(f"<b>🟢 Positive Quality Trend:</b> Top 3 rankings improved by {top_3_change:.1f}%, indicating better content relevance.")
    elif top_3_change < -10:
        insights.append(f"<b>🔴 Authority Concern:</b> Top 3 rankings declined by {abs(top_3_change):.1f}%, suggesting competitive pressure or content issues.")
    
    # Strategic recommendation
    if total_change < 0 and top_10_current_share > top_10_previous_share:
        insights.append("<b>🎯 Quality Focus Strategy:</b> Although you're ranking for fewer total keywords, the higher concentration of top 10 positions suggests a successful focus on high-value terms.")
    elif total_change > 0 and top_10_current_share < top_10_previous_share:
        insights.append("<b>⚠️ Breadth vs Depth Trade-off:</b> You're ranking for more keywords but with lower average positions. Consider consolidating efforts on your best-performing content.")
    
    # Next steps
    if results['bucket_changes']['top_21_plus']['current_share'] > 40:
        insights.append("<b>🎯 Optimization Opportunity:</b> Over 40% of your keywords rank beyond position 20. Focus on improving on-page SEO and building topic authority.")
    
    return "<br><br>".join(insights)

def data_export_instructions():
    """Comprehensive guide for exporting data from various SEO tools"""
    st.markdown('<div class="section-header">📋 Data Export Guide</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>🎯 Quick Reference</h4>
        <p>This guide provides step-by-step instructions for exporting data from <b>Semrush</b>, <b>Google Search Console</b>, and <b>GA4</b>. Follow these instructions to get the exact files needed for each analysis section.</p>
        
        <h4>🔑 Key Rules</h4>
        <ul>
            <li><b>Always export CSV or Excel format</b> - Never PDF</li>
            <li><b>Use consistent naming:</b> client_tool_report_period.csv</li>
            <li><b>Same date ranges</b> across all exports for accuracy</li>
            <li><b>Year-over-year comparisons</b> should use same month from previous year</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create expandable sections for each tool
    with st.expander("🔍 **Semrush Exports** - Keyword Rankings & Competition Data", expanded=True):
        
        st.markdown("### Organic Research → Positions")
        st.markdown("""
        **Use for:** Keyword Visibility Trends, Competitor Analysis
        
        **Steps:**
        1. Go to **Domain Analytics → Organic Research → Positions**
        2. Set **Database** (e.g., United States)
        3. Set **Device = Desktop** 
        4. Set **Date = current month** (for current data)
        5. Click **Export → CSV** or **Excel**
        6. Save as: `client_semrush_positions_YYYY-MM.csv`
        
        **For Year-over-Year Analysis:**
        - Repeat above steps but change **Date** to same month last year
        - Save as: `client_semrush_positions_YYYY-MM_LY.csv`
        """)
        
        st.markdown("### Organic Research → Position Changes")
        st.markdown("""
        **Use for:** Keyword Movement Analysis
        
        **Steps:**
        1. Go to **Organic Research → Position Changes**
        2. Set **Range = Last 12 months** (or desired period)
        3. Click **Export → CSV** or **Excel**
        4. Save as: `client_semrush_position-changes_last12m.csv`
        """)
        
        st.markdown("### Organic Research → Pages")
        st.markdown("""
        **Use for:** Page Performance Analysis
        
        **Steps:**
        1. Go to **Organic Research → Pages**
        2. Set **Date = current month**
        3. Click **Export → CSV** or **Excel**
        4. Save as: `client_semrush_pages_YYYY-MM.csv`
        """)
        
        st.markdown("### Organic Research → Competitors")
        st.markdown("""
        **Use for:** Competitor Gap Analysis
        
        **Steps:**
        1. Go to **Organic Research → Competitors**
        2. Click **Export → CSV** or **Excel**
        3. Save as: `client_semrush_competitors_YYYY-MM.csv`
        """)
        
        st.markdown("### Position Tracking (Optional)")
        st.markdown("""
        **Use for:** SERP Features Analysis (if project exists)
        
        **Steps:**
        1. Go to **Projects → Position Tracking → Overview**
        2. If **AI Overviews** enabled, export that tab too
        3. Click **Export → CSV** or **Excel**
        4. Save as: `client_semrush_tracking_YYYY-MM.csv`
        
        ⚠️ **Note:** Only available if you have an existing Position Tracking project
        """)

    with st.expander("🔎 **Google Search Console Exports** - Click & Impression Data"):
        
        st.markdown("### Search Results - Sitewide Compare")
        st.markdown("""
        **Use for:** Traffic Attribution Analysis
        
        **Steps:**
        1. Go to **Search results** in left navigation
        2. Set top filters:
           - **Search type = Web**
           - **Date → Compare → Last 3 months vs Same period last year → Apply**
        3. Click **Export** (top right) → **CSV** or **Excel**
        4. Save as: `client_gsc_search-results_compare_[dates].csv`
        """)
        
        st.markdown("### Queries - Compare View")
        st.markdown("""
        **Use for:** Query Performance Analysis
        
        **Steps:**
        1. In **Search results**, click **Queries** tab
        2. Ensure **Compare** date setting is still applied from previous step
        3. Click **Export → CSV** or **Excel**
        4. Save as: `client_gsc_queries_compare_[dates].csv`
        """)
        
        st.markdown("### Pages - Compare View")
        st.markdown("""
        **Use for:** Page Performance Analysis (GSC data)
        
        **Steps:**
        1. In **Search results**, click **Pages** tab  
        2. Ensure **Compare** date setting is still applied
        3. Click **Export → CSV** or **Excel**
        4. Save as: `client_gsc_pages_compare_[dates].csv`
        """)
        
        st.markdown("""
        💡 **Pro Tip:** Set up your date comparison once in Search Results, then export all three views (sitewide, queries, pages) with the same date settings for consistency.
        """)

    with st.expander("📊 **GA4 Exports** - Traffic & Conversion Data"):
        
        st.markdown("### Traffic Acquisition - Organic Search Only")
        st.markdown("""
        **Use for:** Traffic Attribution Analysis
        
        **Steps:**
        1. Go to **Reports → Acquisition → Traffic acquisition**
        2. Set **date picker** to same window used in GSC
           - For YoY analysis, use **Compare** to previous year
        3. **Add filter:** Session default channel group = **Organic Search**
        4. Click **Share this report → Download file → CSV**
        5. Save as: `client_ga4_traffic-acquisition_organic_[dates].csv`
        """)
        
        st.markdown("### Landing Page - Organic Search Only")
        st.markdown("""
        **Use for:** Conversion Optimization Analysis
        
        **Steps:**
        1. Go to **Reports → Engagement → Landing page**
        2. Set **date picker** to same window as above
        3. **Add filter:** Session default channel group = **Organic Search**  
        4. Click **Share this report → Download file → CSV**
        5. Save as: `client_ga4_landing-page_organic_[dates].csv`
        """)
        
        st.markdown("### If Landing Page Report Missing")
        st.markdown("""
        **Alternative: Build Custom Exploration**
        
        1. Go to **Explore** → **+ Blank exploration**
        2. **Name it:** Landing Page -- Organic Search
        3. **Add dimension:** Landing page + query string
        4. **Add metrics:** Sessions, Active users, Engaged sessions, Average engagement time, Key events
        5. **Add filter:** Session default channel group = "Organic Search"
        6. **Export:** Top right → Export → CSV
        
        This creates the same data as the standard Landing Page report.
        """)

    with st.expander("✅ **File Validation Checklist**"):
        st.markdown("""
        Before uploading your files, verify:
        
        **✅ Format Requirements:**
        - Files are in CSV or Excel format (never PDF)
        - Column headers are present and readable
        - Data contains expected metrics (clicks, impressions, positions, etc.)
        
        **✅ Date Consistency:**
        - All files use the same date ranges
        - Year-over-year comparisons use same month from previous year
        - Compare periods match between GSC and GA4 exports
        
        **✅ File Naming:**
        - Clear, consistent naming convention
        - Include client, tool, report type, and date period
        - Example: `acme_semrush_positions_2024-08.csv`
        
        **✅ Data Quality:**
        - Files contain data (not empty exports)
        - Position data is numeric (not text)
        - Keyword/Query lists are complete
        """)

    with st.expander("🆘 **Troubleshooting Common Issues**"):
        st.markdown("""
        **"Column not found" errors:**
        - Column names vary between exports - the tool auto-detects most variations
        - Ensure you're exporting from the correct section (Positions vs Position Changes)
        - Check that headers are in English (not localized)
        
        **Excel files won't upload:**
        - Try exporting as CSV instead
        - Ensure file isn't password protected
        - Check file size (very large files may timeout)
        
        **Missing data in analysis:**
        - Verify date ranges match between current and previous exports
        - Some tools have data limitations (GSC keeps ~16 months)
        - Position Tracking requires existing project setup
        
        **GSC Compare issues:**
        - Use "Same period last year" not custom date ranges
        - Ensure you're comparing like periods (3 months vs 3 months)
        - Web search type should be selected
        
        **GA4 Filter problems:**
        - Use exact text "Organic Search" for channel group filter
        - Default channel group is different from source/medium
        - Some accounts have custom channel definitions
        """)

    st.markdown("---")
    st.success("💡 **Ready to start?** Choose an analysis tab above and follow the specific file requirements for each section!")

def keyword_movement_analysis():
    """Analyze keyword movement distribution from Semrush Position Changes"""
    st.markdown('<div class="section-header">🔄 Keyword Movement Distribution</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis examines how your keyword rankings changed over time to identify:</p>
        <ul>
            <li><b>Movement distribution</b> - How many keywords improved, declined, or stayed unchanged</li>
            <li><b>Top winners and losers</b> - Specific keywords with biggest ranking changes</li>
            <li><b>Improved:Declined ratio</b> - Overall trend momentum indicator</li>
            <li><b>Ranking flow analysis</b> - Where keywords moved between ranking buckets</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>1 Semrush Position Changes file</b>:</p>
        <ul>
            <li><b>Position Changes export</b> from Semrush (last 12 months recommended)</li>
            <li>Must include: Keyword, Position, Previous Position columns</li>
            <li>Optional: URL column for additional context</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Movement distribution with improved:declined ratio</li>
            <li>Top improving keywords (prioritizing #1 rankings)</li>
            <li>Top declining keywords requiring attention</li>
            <li>Ranking flow between position buckets (Top 3, 4-10, etc.)</li>
            <li>Sources of new top 3 rankings</li>
        </ul>
        
        <h4>🔍 Methodology Note:</h4>
        <p>This analysis treats <b>Position = 0 as "not ranked"</b> (worst position). This means:</p>
        <ul>
            <li>Falling out of rankings (→0) counts as <b>Declined</b></li>
            <li>Newly ranked keywords (0→#) count as <b>Improved</b></li>
            <li>Movement calculation excludes artificial cases</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="file-upload-section">', unsafe_allow_html=True)
    st.markdown("#### 📤 Upload Position Changes Data")
    
    position_changes_file = st.file_uploader(
        "Upload Semrush Position Changes file",
        type=['csv', 'xlsx', 'xls'],
        key="position_changes",
        help="Export from Semrush: Organic Research → Position Changes (CSV or Excel format)"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process file if uploaded
    if position_changes_file is not None:
        # Add Run Analysis button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Run Movement Analysis", key="run_movement", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing keyword movements..."):
                    try:
                        # Load and validate data
                        df = normalize_columns(read_uploaded_file(position_changes_file))
                        
                        # Validate required columns
                        validation_passed, validation_message = validate_movement_data(df)
                        
                        if not validation_passed:
                            st.markdown(f'<div class="warning-box">{validation_message}</div>', unsafe_allow_html=True)
                            return
                        
                        # Perform analysis
                        movement_results = analyze_keyword_movement(df)
                        
                        # Display results
                        display_movement_results(movement_results)
                        
                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")
                        st.info("💡 Please ensure you've uploaded a valid Semrush Position Changes file")
    else:
        st.info("📤 Please upload a Semrush Position Changes file to begin analysis")

def validate_movement_data(df):
    """Validate the Position Changes data"""
    required_columns = ['Keyword', 'Position', 'Previous position']
    
    # Find columns using flexible matching
    kw_col = find_column(df.columns, ['keyword'])
    pos_col = find_column(df.columns, ['position']) 
    prev_pos_col = find_column(df.columns, ['previous position', 'prev position', 'previous'])
    
    missing_columns = []
    if not kw_col:
        missing_columns.append('Keyword')
    if not pos_col:
        missing_columns.append('Position')  
    if not prev_pos_col:
        missing_columns.append('Previous Position')
    
    if missing_columns:
        return False, f"❌ Missing required columns: {missing_columns}. Available columns: {list(df.columns)[:10]}"
    
    # Check if data is not empty
    if len(df) == 0:
        return False, "❌ File appears to be empty"
    
    return True, "✅ Data validation passed"

def analyze_keyword_movement(df):
    """Analyze keyword movement patterns"""
    
    # Find and rename columns
    kw_col = find_column(df.columns, ['keyword'])
    pos_col = find_column(df.columns, ['position'])
    prev_pos_col = find_column(df.columns, ['previous position', 'prev position', 'previous'])
    url_col = find_column(df.columns, ['url', 'page', 'landing page'])
    
    # Prepare working dataframe
    work_df = pd.DataFrame()
    work_df['Keyword'] = df[kw_col].astype(str).str.strip()
    work_df['Position'] = pd.to_numeric(df[pos_col], errors='coerce')
    work_df['Previous_Position'] = pd.to_numeric(df[prev_pos_col], errors='coerce')
    
    if url_col:
        work_df['URL'] = df[url_col].astype(str)
    
    # Remove rows with missing position data
    work_df = work_df.dropna(subset=['Position', 'Previous_Position'])
    
    # Calculate movement (real numbers for tables)
    work_df['Movement'] = work_df['Previous_Position'] - work_df['Position']  # positive = improved rank
    
    # Status classification treating 0 as "not ranked" (worst)
    def effective_rank(series):
        return np.where((series <= 0) | pd.isna(series), 1000, series)
    
    eff_prev = effective_rank(work_df['Previous_Position'])
    eff_now = effective_rank(work_df['Position'])
    status_movement = eff_prev - eff_now  # >0 improved, <0 declined, =0 unchanged
    
    work_df['Status'] = np.where(status_movement > 0, 'Improved',
                        np.where(status_movement < 0, 'Declined', 'Unchanged'))
    
    # Movement distribution
    counts = work_df['Status'].value_counts().reindex(['Improved', 'Declined', 'Unchanged']).fillna(0).astype(int)
    improved, declined, unchanged = int(counts.get('Improved', 0)), int(counts.get('Declined', 0)), int(counts.get('Unchanged', 0))
    ratio = (improved / declined) if declined > 0 else np.inf
    
    # Top improvers (exclude Position=0, prioritize #1)
    improved_df = work_df[(work_df['Movement'] > 0) & (work_df['Position'] > 0)].copy()
    improved_df['Reached_1'] = (improved_df['Position'] == 1).astype(int)
    top_improvers = improved_df.sort_values(['Reached_1', 'Movement'], ascending=[False, False]).head(25)
    
    # Top decliners (exclude Previous_Position=0, keep drops to 0)
    declined_df = work_df[(work_df['Movement'] < 0) & (work_df['Previous_Position'] > 0)].copy()
    top_decliners = declined_df.sort_values('Movement', ascending=True).head(25)
    
    # Bucket analysis
    def bucketize_position(series):
        return pd.cut(series, bins=[-np.inf, 0, 3, 10, 20, np.inf], 
                     labels=['Invalid', 'Top 1-3', '4-10', '11-20', '21+'], right=True)
    
    bucket_order = ['Top 1-3', '4-10', '11-20', '21+']
    work_df['Prev_Bucket'] = bucketize_position(work_df['Previous_Position'])
    work_df['Now_Bucket'] = bucketize_position(work_df['Position'])
    
    # Filter valid buckets for transition analysis
    bucket_df = work_df[(work_df['Prev_Bucket'] != 'Invalid') & (work_df['Now_Bucket'] != 'Invalid')].copy()
    
    # Transition matrix
    transition_matrix = pd.crosstab(bucket_df['Prev_Bucket'], bucket_df['Now_Bucket']).reindex(index=bucket_order, columns=bucket_order, fill_value=0)
    
    # Net flow analysis
    diagonal = pd.Series({b: transition_matrix.at[b, b] if (b in transition_matrix.index and b in transition_matrix.columns) else 0 for b in bucket_order})
    inflow = transition_matrix.sum(axis=0) - diagonal
    outflow = transition_matrix.sum(axis=1) - diagonal
    net_flow = inflow.reindex(bucket_order) - outflow.reindex(bucket_order)
    
    prev_counts = transition_matrix.sum(axis=1).reindex(bucket_order)
    now_counts = transition_matrix.sum(axis=0).reindex(bucket_order)
    delta_counts = now_counts - prev_counts
    
    # Sources of new Top 1-3
    new_top3 = bucket_df[bucket_df['Now_Bucket'] == 'Top 1-3']
    top3_sources = new_top3['Prev_Bucket'].value_counts().reindex(bucket_order, fill_value=0)
    
    return {
        'total_keywords': len(work_df),
        'movement_counts': {'improved': improved, 'declined': declined, 'unchanged': unchanged},
        'ratio': ratio,
        'top_improvers': top_improvers,
        'top_decliners': top_decliners,
        'transition_matrix': transition_matrix,
        'bucket_flow': {
            'prev_counts': prev_counts,
            'now_counts': now_counts, 
            'delta_counts': delta_counts,
            'inflow': inflow.reindex(bucket_order),
            'outflow': outflow.reindex(bucket_order),
            'net_flow': net_flow
        },
        'top3_sources': top3_sources,
        'raw_data': work_df
    }

def display_movement_results(results):
    """Display keyword movement analysis results"""
    
    # Key metrics
    st.markdown('<div class="section-header">📈 Movement Distribution Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Keywords Analyzed",
            value=f"{results['total_keywords']:,}"
        )
    
    with col2:
        st.metric(
            label="Improved Rankings",
            value=f"{results['movement_counts']['improved']:,}",
            delta=f"+{results['movement_counts']['improved']:,} keywords"
        )
    
    with col3:
        st.metric(
            label="Declined Rankings", 
            value=f"{results['movement_counts']['declined']:,}",
            delta=f"-{results['movement_counts']['declined']:,} keywords",
            delta_color="inverse"
        )
    
    with col4:
        ratio_display = f"{results['ratio']:.2f}" if results['ratio'] != np.inf else "∞"
        st.metric(
            label="Improved:Declined Ratio",
            value=ratio_display,
            help="Higher ratio indicates more keywords improving than declining"
        )
    
    # Distribution chart
    st.markdown('<div class="section-header">📊 Movement Distribution</div>', unsafe_allow_html=True)
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Bar chart of movement distribution
        dist_data = results['movement_counts']
        fig_dist = go.Figure(data=[
            go.Bar(x=list(dist_data.keys()), 
                   y=list(dist_data.values()),
                   marker_color=['#2ecc71', '#e74c3c', '#95a5a6'],
                   text=list(dist_data.values()),
                   textposition='auto'
            )
        ])
        
        fig_dist.update_layout(
            title='Keyword Movement Distribution',
            xaxis_title='Movement Type',
            yaxis_title='Number of Keywords',
            height=400
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with viz_col2:
        # Pie chart of movement share
        labels = list(results['movement_counts'].keys())
        values = list(results['movement_counts'].values())
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=['#2ecc71', '#e74c3c', '#95a5a6']
        )])
        
        fig_pie.update_layout(
            title='Movement Distribution Share',
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Top winners and losers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">🏆 Top Improving Keywords</div>', unsafe_allow_html=True)
        st.markdown("*Keywords with biggest positive movement (prioritizing new #1 rankings)*")
        
        if not results['top_improvers'].empty:
            display_cols = ['Keyword', 'Previous_Position', 'Position', 'Movement']
            if 'URL' in results['top_improvers'].columns:
                display_cols.append('URL')
            
            improvers_display = results['top_improvers'][display_cols].head(15).copy()
            improvers_display.columns = ['Keyword', 'Previous Pos', 'Current Pos', 'Movement'] + (['URL'] if 'URL' in display_cols else [])
            st.dataframe(improvers_display, use_container_width=True, hide_index=True)
        else:
            st.info("No improving keywords found with the current criteria")
    
    with col2:
        st.markdown('<div class="section-header">📉 Top Declining Keywords</div>', unsafe_allow_html=True)
        st.markdown("*Keywords with biggest negative movement (excluding newly ranked keywords)*")
        
        if not results['top_decliners'].empty:
            display_cols = ['Keyword', 'Previous_Position', 'Position', 'Movement']
            if 'URL' in results['top_decliners'].columns:
                display_cols.append('URL')
            
            decliners_display = results['top_decliners'][display_cols].head(15).copy()
            decliners_display.columns = ['Keyword', 'Previous Pos', 'Current Pos', 'Movement'] + (['URL'] if 'URL' in display_cols else [])
            st.dataframe(decliners_display, use_container_width=True, hide_index=True)
        else:
            st.info("No declining keywords found with the current criteria")
    
    # Bucket flow analysis
    st.markdown('<div class="section-header">🔄 Ranking Bucket Flow Analysis</div>', unsafe_allow_html=True)
    
    # Transition matrix
    st.markdown("**Transition Matrix - Previous Bucket → Current Bucket**")
    st.dataframe(results['transition_matrix'], use_container_width=True)
    
    # Net flow table
    st.markdown("**Net Movement by Ranking Bucket**")
    flow_table = pd.DataFrame({
        'Ranking Bucket': results['bucket_flow']['prev_counts'].index,
        'Previous Count': results['bucket_flow']['prev_counts'].values,
        'Current Count': results['bucket_flow']['now_counts'].values,
        'Change': results['bucket_flow']['delta_counts'].values,
        'Inflow': results['bucket_flow']['inflow'].values,
        'Outflow': results['bucket_flow']['outflow'].values,
        'Net Flow': results['bucket_flow']['net_flow'].values
    })
    
    st.dataframe(flow_table, use_container_width=True, hide_index=True)
    
    # Sources of new top 3 rankings
    if not results['top3_sources'].empty:
        st.markdown("**Sources of New Top 1-3 Rankings**")
        sources_df = pd.DataFrame({
            'Previous Bucket': results['top3_sources'].index,
            'Keywords Moved to Top 1-3': results['top3_sources'].values
        })
        st.dataframe(sources_df, use_container_width=True, hide_index=True)
    
    # Strategic insights
    st.markdown('<div class="section-header">💡 Strategic Insights</div>', unsafe_allow_html=True)
    insights = generate_movement_insights(results)
    st.markdown(f'<div class="insight-box">{insights}</div>', unsafe_allow_html=True)
    
    # Download section
    st.markdown('<div class="section-header">📥 Download Results</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        summary_report = create_movement_summary_report(results)
        st.download_button(
            label="📄 Download Movement Analysis Report",
            data=summary_report,
            file_name=f"keyword_movement_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col2:
        # Convert top movers to CSV
        csv_buffer = io.StringIO()
        combined_movers = pd.concat([
            results['top_improvers'].head(15).assign(Type='Improver'),
            results['top_decliners'].head(15).assign(Type='Decliner')
        ])
        combined_movers.to_csv(csv_buffer, index=False)
        
        st.download_button(
            label="📊 Download Top Movers (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"keyword_top_movers_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def generate_movement_insights(results):
    """Generate strategic insights from movement analysis"""
    insights = []
    
    ratio = results['ratio']
    improved = results['movement_counts']['improved']
    declined = results['movement_counts']['declined']
    
    # Overall trend analysis
    if ratio > 1.5:
        insights.append(f"<b>🟢 Strong Upward Momentum:</b> With {improved:,} improving vs {declined:,} declining keywords (ratio: {ratio:.2f}), your overall keyword portfolio is strengthening significantly.")
    elif ratio > 1.0:
        insights.append(f"<b>🟢 Positive Trend:</b> More keywords improving ({improved:,}) than declining ({declined:,}), indicating healthy SEO momentum.")
    elif ratio > 0.8:
        insights.append(f"<b>🟡 Mixed Results:</b> Nearly balanced movement with {improved:,} improving vs {declined:,} declining. Focus on protecting top performers.")
    else:
        insights.append(f"<b>🔴 Declining Trend:</b> More keywords declining ({declined:,}) than improving ({improved:,}). Priority should be stabilizing rankings and identifying causes.")
    
    # Top 3 analysis
    if not results['top3_sources'].empty:
        top_source = results['top3_sources'].idxmax()
        top_count = results['top3_sources'].max()
        insights.append(f"<b>🎯 Top 3 Growth:</b> Most new top 3 rankings ({top_count}) came from the {top_source} bucket, showing your ability to push mid-performing keywords to elite positions.")
    
    # Bucket flow insights
    flow = results['bucket_flow']
    top3_net = flow['net_flow']['Top 1-3'] if 'Top 1-3' in flow['net_flow'].index else 0
    tail_net = flow['net_flow']['21+'] if '21+' in flow['net_flow'].index else 0
    
    if top3_net > 0 and tail_net < 0:
        insights.append("<b>🎯 Quality Consolidation:</b> You're successfully moving keywords from the long tail into top positions - a sign of content optimization working.")
    elif top3_net < 0:
        insights.append("<b>⚠️ Top Position Pressure:</b> You're losing some top 3 rankings. Review competitors and refresh your highest-value content.")
    
    # Actionable recommendations
    if results['movement_counts']['declined'] > 0:
        insights.append(f"<b>🔧 Action Items:</b> Review the {min(15, results['movement_counts']['declined'])} top declining keywords shown above. Look for content freshness, competitor analysis, and technical issues.")
    
    return "<br><br>".join(insights)

def create_movement_summary_report(results):
    """Create downloadable movement analysis report"""
    
    ratio_display = f"{results['ratio']:.2f}" if results['ratio'] != np.inf else "∞"
    
    report = f"""
KEYWORD MOVEMENT ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

===========================================
EXECUTIVE SUMMARY
===========================================

Total Keywords Analyzed: {results['total_keywords']:,}

Movement Distribution:
• Improved Rankings: {results['movement_counts']['improved']:,} keywords
• Declined Rankings: {results['movement_counts']['declined']:,} keywords  
• Unchanged Rankings: {results['movement_counts']['unchanged']:,} keywords
• Improved:Declined Ratio: {ratio_display}

===========================================
TOP IMPROVING KEYWORDS (Sample)
===========================================

"""
    
    if not results['top_improvers'].empty:
        for _, row in results['top_improvers'].head(10).iterrows():
            report += f"• {row['Keyword']} | {row['Previous_Position']} → {row['Position']} (+{row['Movement']:.0f})\n"
    
    report += f"""

===========================================
TOP DECLINING KEYWORDS (Sample)
===========================================

"""
    
    if not results['top_decliners'].empty:
        for _, row in results['top_decliners'].head(10).iterrows():
            report += f"• {row['Keyword']} | {row['Previous_Position']} → {row['Position']} ({row['Movement']:.0f})\n"
    
    report += f"""

===========================================
RANKING BUCKET FLOW ANALYSIS
===========================================

Bucket Changes:
"""
    
    for bucket in results['bucket_flow']['prev_counts'].index:
        prev_count = results['bucket_flow']['prev_counts'][bucket]
        now_count = results['bucket_flow']['now_counts'][bucket] 
        change = results['bucket_flow']['delta_counts'][bucket]
        report += f"• {bucket}: {prev_count} → {now_count} ({change:+})\n"
    
    report += f"""

===========================================
STRATEGIC INSIGHTS
===========================================

{generate_movement_insights(results).replace('<b>', '').replace('</b>', '').replace('<br><br>', '\n\n').replace('🟢', '• ').replace('🟡', '• ').replace('🔴', '• ').replace('🎯', '• ').replace('⚠️', '• ').replace('🔧', '• ')}

===========================================
"""
    
    return report

def page_performance_analysis():
    """Analyze page performance from Semrush Pages data"""
    st.markdown('<div class="section-header">📄 Page Performance Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis examines your top-performing pages to understand:</p>
        <ul>
            <li><b>Traffic concentration</b> - How much traffic comes from your top pages (Pareto analysis)</li>
            <li><b>Efficiency metrics</b> - Traffic per keyword to identify high-performing content</li>
            <li><b>Directory clustering</b> - Which content hubs drive the most organic traffic</li>
            <li><b>Long-tail opportunities</b> - Pages with many keywords but low efficiency</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>1 Semrush Pages file</b>:</p>
        <ul>
            <li><b>Pages export</b> from Semrush Organic Research (current period)</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Pages needed to reach 50%, 80%, 90% of traffic</li>
            <li>Traffic efficiency leaderboard (traffic per keyword)</li>
            <li>Content hub analysis by directory</li>
            <li>Long-tail optimization opportunities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This section will include Pareto analysis, efficiency metrics, and directory clustering from your prototype!")

def query_gains_losses_analysis():
    """Analyze query-level gains and losses from GSC"""
    st.markdown('<div class="section-header">🎯 Query Performance Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis examines search query performance to identify:</p>
        <ul>
            <li><b>Top winning queries</b> - Search terms driving the most additional clicks</li>
            <li><b>Top losing queries</b> - Search terms losing traffic that need attention</li>
            <li><b>CTR vs impression changes</b> - Separate demand growth from execution issues</li>
            <li><b>SERP feature impact</b> - Queries affected by rich snippets, AI overviews, etc.</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>1-2 files</b>:</p>
        <ul>
            <li><b>GSC Queries Compare</b> - Primary analysis file</li>
            <li><b>Semrush Positions (current)</b> - Optional enrichment for position context</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Biggest query-level winners and losers</li>
            <li>CTR pressure vs ranking wins identification</li>
            <li>Charts showing top movers</li>
            <li>Position-enriched analysis when available</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This section will analyze GSC query data with your mixed charts + tables approach!")

def competitor_analysis():
    """Analyze competitor rankings and gaps"""
    st.markdown('<div class="section-header">🏁 Competitor Gap Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis examines your competitive landscape to understand:</p>
        <ul>
            <li><b>Top search competitors</b> - Domains most similar to yours in SERPs</li>
            <li><b>Ranking gaps</b> - Keywords where competitors outrank you</li>
            <li><b>Competitive pressure</b> - Which competitors affect your top losing queries</li>
            <li><b>Gap opportunities</b> - Specific keywords to target for competitive gains</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>2+ files</b>:</p>
        <ul>
            <li><b>Semrush Competitors</b> - List of your top competitors</li>
            <li><b>Your Positions (current)</b> - Your current keyword rankings</li>
            <li><b>Competitor Positions</b> - Optional: competitor ranking data for detailed gaps</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Top competitors by relevance/overlap</li>
            <li>Outrank counts for each competitor</li>
            <li>Focus on losing queries where competitors beat you</li>
            <li>Mini gap tables for specific opportunities</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This section will show competitor outranking analysis with your gap table methodology!")

def traffic_attribution_analysis():
    """Analyze sitewide traffic attribution from GSC"""
    st.markdown('<div class="section-header">📈 Traffic Attribution Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instruction-box">
        <h4>📋 What This Section Analyzes:</h4>
        <p>This analysis examines your overall organic performance to understand:</p>
        <ul>
            <li><b>Sitewide clicks & impressions</b> - Total organic performance YoY</li>
            <li><b>CTR trends</b> - Whether click-through rates are improving</li>
            <li><b>Position changes</b> - Average ranking movement impact</li>
            <li><b>Demand vs execution</b> - Separate impression growth from CTR issues</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>1-2 files</b>:</p>
        <ul>
            <li><b>GSC Search Results Compare</b> - Sitewide performance comparison</li>
            <li><b>GA4 Traffic Acquisition</b> - Optional: validate organic session impact</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Total clicks and impressions YoY changes</li>
            <li>Weighted CTR and position analysis</li>
            <li>Traffic pattern interpretation</li>
            <li>Business impact validation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This section will analyze sitewide GSC performance with weighted metrics!")

def create_visibility_summary_report(results):
    """Create a downloadable summary report"""
    
    report = f"""
KEYWORD VISIBILITY ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

===========================================
EXECUTIVE SUMMARY
===========================================

Total Keywords Comparison:
• Previous Period: {results['total_previous']:,} keywords
• Current Period: {results['total_current']:,} keywords
• Change: {results['total_change']:,} keywords ({results['total_change_pct']:.1f}%)

Ranking Quality Distribution (Current Period):
• Top 3 Positions: {results['bucket_changes']['top_3']['current']} ({results['bucket_changes']['top_3']['current_share']:.1f}%)
• Positions 4-10: {results['bucket_changes']['top_4_10']['current']} ({results['bucket_changes']['top_4_10']['current_share']:.1f}%)
• Positions 11-20: {results['bucket_changes']['top_11_20']['current']} ({results['bucket_changes']['top_11_20']['current_share']:.1f}%)
• Positions 21+: {results['bucket_changes']['top_21_plus']['current']} ({results['bucket_changes']['top_21_plus']['current_share']:.1f}%)

===========================================
DETAILED CHANGES BY RANKING BUCKET
===========================================

Top 3 Rankings:
• Previous: {results['bucket_changes']['top_3']['previous']} | Current: {results['bucket_changes']['top_3']['current']}
• Change: {results['bucket_changes']['top_3']['change']} ({results['bucket_changes']['top_3']['change_pct']:.1f}%)

Positions 4-10:
• Previous: {results['bucket_changes']['top_4_10']['previous']} | Current: {results['bucket_changes']['top_4_10']['current']}
• Change: {results['bucket_changes']['top_4_10']['change']} ({results['bucket_changes']['top_4_10']['change_pct']:.1f}%)

Positions 11-20:
• Previous: {results['bucket_changes']['top_11_20']['previous']} | Current: {results['bucket_changes']['top_11_20']['current']}
• Change: {results['bucket_changes']['top_11_20']['change']} ({results['bucket_changes']['top_11_20']['change_pct']:.1f}%)

Positions 21+:
• Previous: {results['bucket_changes']['top_21_plus']['previous']} | Current: {results['bucket_changes']['top_21_plus']['current']}
• Change: {results['bucket_changes']['top_21_plus']['change']} ({results['bucket_changes']['top_21_plus']['change_pct']:.1f}%)

===========================================
RECOMMENDATIONS
===========================================

{generate_visibility_insights(results).replace('<b>', '').replace('</b>', '').replace('<br><br>', '\n\n').replace('🟢', '• ').replace('🟡', '• ').replace('🔴', '• ').replace('🟨', '• ').replace('🎯', '• ').replace('⚠️', '• ')}

===========================================
"""
    return report

if __name__ == "__main__":
    main()
