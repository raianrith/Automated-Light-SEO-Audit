import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Visibility Trends", 
        "🔄 Keyword Movement", 
        "📄 Page Performance",
        "🎯 Query Analysis",
        "🏁 Competitor Gaps",
        "📈 Traffic Attribution", 
        "🚧 More Soon"
    ])
    
    with tab1:
        keyword_visibility_analysis()
        
    with tab2:
        keyword_movement_analysis()
        
    with tab3:
        page_performance_analysis()
        
    with tab4:
        query_gains_losses_analysis()
        
    with tab5:
        competitor_analysis()
        
    with tab6:
        traffic_attribution_analysis()
        
    with tab7:
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
            "Upload current Semrush Positions CSV",
            type=['csv'],
            key="current_positions",
            help="Export from Semrush: Domain Analytics → Organic Research → Positions"
        )
        
    with col2:
        st.markdown("#### 📤 Previous Period (Same Month Last Year)")
        previous_file = st.file_uploader(
            "Upload previous year Semrush Positions CSV", 
            type=['csv'],
            key="previous_positions",
            help="Same export but for the corresponding month last year"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process files if both are uploaded
    if current_file is not None and previous_file is not None:
        with st.spinner("🔄 Processing your data..."):
            try:
                # Load data
                current_df = pd.read_csv(current_file)
                previous_df = pd.read_csv(previous_file)
                
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
                st.info("💡 Please ensure you've uploaded valid Semrush Positions CSV files")

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
            <li><b>Improved:Declined ratio</b> - Overall trend momentum</li>
            <li><b>Ranking flow analysis</b> - Where keywords moved between ranking buckets</li>
        </ul>
        
        <h4>📁 Required Files:</h4>
        <p>You need <b>1 Semrush Position Changes file</b>:</p>
        <ul>
            <li><b>Position Changes export</b> from Semrush (last 12 months recommended)</li>
        </ul>
        
        <h4>🎯 Key Insights You'll Get:</h4>
        <ul>
            <li>Movement distribution with improved:declined ratio</li>
            <li>Top improving keywords (prioritizing #1 rankings)</li>
            <li>Top declining keywords requiring attention</li>
            <li>Ranking flow between position buckets</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This section is coming next! Based on your Colab prototype's keyword movement analysis.")

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
