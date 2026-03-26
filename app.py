# This app visualizes key business insights from the SuperStore dataset.
# Built for portfolio demonstration - Analytics/IT/Finance internship target

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# PAGE CONFIGURATION
# This MUST be the first Streamlit command - sets up the browser tab/window
st.set_page_config(
    page_title="SuperStore Analysis",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS STYLING
# This adds padding and makes the app look more polished
st.markdown("""
    <style>
    /* Add padding to main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 5rem;
        padding-right: 10rem;
    }
    
    /* Add spacing after headers */
    h1, h2, h3 {
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Add padding to sidebar */
    .sidebar-content {
        padding-top: 4rem;
    }
    
    /* Add spacing between expander sections */
    .streamlit-expanderContent {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# LOAD DATA
# Using @st.cache_data - Streamlit caches this so it only loads ONCE
# This makes the app much faster on refresh
@st.cache_data
def load_data():
    """Load and preprocess the SuperStore dataset"""
    df = pd.read_csv(
        'data/superstore_data.csv', 
        encoding='latin1', 
        low_memory=False
    )
    
    # Convert data types
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    
    return df

# Load the data
df = load_data()

# SIDEBAR NAVIGATION
# st.sidebar creates the left sidebar - perfect for navigation!
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

# Create radio buttons for tab selection
tab = st.sidebar.radio(
    "Select a Tab:",
    [
        "Home",
        "Category Profit",
        "Region Analysis", 
        "Discount vs Profit",
        "Product Margins",
        "Monthly Trend"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    
    Built by: Ira Herrera
    
    Purpose: Portfolio project for Analytics/IT/Finance internships
    
    Dataset: SuperStore (Kaggle)
    """
)

# HOME PAGE
if tab == "Home":
    st.title("SuperStore Sales Analysis")
    st.markdown("---")
    
    # Introduction
    st.header("Welcome!")
    st.write("""
    This interactive dashboard explores key business questions using the SuperStore dataset.
    Use the **sidebar** to navigate through each analysis.
    """)
    
    # Key metrics row (impressive for portfolios!)
    st.header("Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sales", 
            value=f"${df['Sales'].sum():,.0f}"
        )
    
    with col2:
        st.metric(
            label="Total Profit", 
            value=f"${df['Profit'].sum():,.0f}"
        )
    
    with col3:
        st.metric(
            label="Total Orders", 
            value=f"{df['Order ID'].nunique():,}"
        )
    
    with col4:
        st.metric(
            label="Avg Profit Margin", 
            value=f"{(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%"
        )
    
    st.markdown("---")
    
    # Show data preview option
    with st.expander("📋 View Raw Data"):
        st.dataframe(df.head(100), hide_index=True)
        st.caption(f"Showing first 100 rows of {len(df):,} total records")

# QUESTION 1: Category Profit
elif tab == "Category Profit":
    st.title("Which Category Makes the Most Profit?")
    st.markdown("---")
    
    # Calculate category profit (same as your notebook)
    cat_profit = df.groupby('Category')['Profit'].sum().reset_index()
    cat_profit = cat_profit.sort_values('Profit', ascending=False)
    
    # Display insight
    st.subheader("Key Insight")
    winner = cat_profit.iloc[0]
    st.success(
        f"**{winner['Category']}** leads with **${winner['Profit']:,.2f}** in profit!"
    )
    st.warning(
        f'**Tech** has a high concentration risk, if tech category faces and issues, over 50% of profit is vulnerable. \nFurniture generates only about 6% of profit despite likely needint significant storage space, consider reducing furniture inventory drastically and reallocating resources gained towards leading categories.' 
    )
    
    # Create the bar chart
    fig = px.bar(
        cat_profit,
        x='Category',
        y='Profit',
        title='Profit by Category',
        labels={'Category': 'Product Category', 'Profit': 'Profit ($)'},
        color='Profit',
        color_continuous_scale='Greens',
        text_auto='.2s'
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title=None
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    with st.expander("View Data"):
        st.dataframe(cat_profit.style.format({'Profit': '${:,.2f}'}), hide_index=True)

# QUESTION 2: Region Analysis
elif tab == "Region Analysis":
    st.title("Which Region Sells the most & which profits the least?")
    st.markdown("---")
    
    # Calculate region data
    region_data = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    region_data['Profit_Margin'] = (
        region_data['Profit'] / region_data['Sales'] * 100
    ).round(2)
    
    # Display insights
    st.subheader("Key Insights")
    col1, col2 = st.columns(2)
    
    st.subheader('Oppurtunity')
    st.write("""**Central Region Problem:**  \n-3rd highest sales (500k), but lowest profits($40k).  \n-Margin is 7% BELOW company average.  \n-If central achieved East\'s margin, additional $28k+ profit.""")
    st.write("""**South Region Oppurtunity:**  \n-Lowest sales volume suggesting underpenetrated market  \n-Decent margins means profitable when sold.  \n-Growth potential: allocate additional marketing spend to this region""")
    
    with col1:
        highest_sales = region_data.loc[region_data['Sales'].idxmax()]
        st.info(
            f"**Highest Sales:** {highest_sales['Region']} "
            f"(${highest_sales['Sales']:,.2f})"
        )
    
    with col2:
        lowest_profit = region_data.loc[region_data['Profit'].idxmin()]
        st.warning(
            f"**Lowest Profit:** {lowest_profit['Region']} "
            f"(${lowest_profit['Profit']:,.2f})"
        )
    
    # Prepare data for grouped bar chart
    region_melted = region_data.melt(
        id_vars=['Region'],
        value_vars=['Sales', 'Profit'],
        var_name='Metric',
        value_name='Amount'
    )
    
    # Create grouped bar chart
    fig2 = px.bar(
        region_melted,
        x='Region',
        y='Amount',
        color='Metric',
        barmode='group',
        title='Sales vs Profit by Region',
        color_discrete_map={'Sales': "#388ac5", 'Profit': "#49ac49"},
        text_auto='.2s'
    )
    
    fig2.update_layout(height=450, yaxis_title='Amount ($)')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Show data table
    with st.expander("View Data"):
        st.dataframe(
            region_data.style.format({
                'Sales': '${:,.2f}',
                'Profit': '${:,.2f}',
                'Profit_Margin': '{:.2f}%'
            }),
            hide_index=True
        )

# QUESTION 3: Discount vs Profit
elif tab == "Discount vs Profit":
    st.title("How Does Discount Affect Profit?")
    st.markdown("---")
    
    # Calculate correlation
    correlation = df['Profit'].corr(df['Discount'])
    
    # Display insight
    st.subheader("Key Insight")
    
    # Interpret correlation
    if correlation < -0.3:
        interpretation = "Strong NEGATIVE correlation"
        emoji = "🔴"
    elif correlation < 0:
        interpretation = "Weak NEGATIVE correlation"
        emoji = "🟡"
    else:
        interpretation = "Positive correlation"
        emoji = "🟢"
    
    st.metric(
        label="Correlation Coefficient",
        value=f"{correlation:.4f}",
        delta=f"{correlation*100:.1f}%"
    )
    
    st.write(f"""
    {emoji} **Interpretation:** 
    \n{interpretation}. 
    -For every 10% discount offered, profit tends to decrease by 
    {abs(correlation)*10:.1f}%.\n-Discounts under 20% show minimal profit erosion.\nReducing average discount could drive a profit increase, with the inherent risk of a drop in volume. 
    """)
    
    # Filter outliers for better visualization
    Discount_df = df[df['Profit'].between(-2000, 2000, inclusive='neither')]
    
    with st.expander("View Scatter Plot with Trendline"):
        # Create scatter plot
        fig = px.scatter(
            Discount_df,
            x='Discount',
            y='Profit',
            title='Discount vs Profit Relationship',
            opacity=0.4,
            trendline='ols',
            height=500
        )
        
        fig.update_layout(
            xaxis_title='Discount Rate',
            yaxis_title='Profit ($)'
        )
        
        st.plotly_chart(fig, use_container_width=True)


# QUESTION 4: Product Margins
elif tab == "Product Margins":
    st.title("Top 5 & Bottom 5 Products by Profit Margin")
    st.markdown("---")
    
    # Calculate product margins
    product_margin = df.groupby('Product Name').agg({
        'Profit': 'sum',
        'Sales': 'sum'
    }).reset_index()
    
    product_margin['Margin_Percent'] = (
        product_margin['Profit'] / product_margin['Sales'] * 100
    ).round(2)
    
    # Get top and bottom 5
    top5 = product_margin.sort_values('Margin_Percent', ascending=False).head(5)
    bottom5 = product_margin.sort_values('Margin_Percent', ascending=True).head(5)
    
    # Display insights
    st.subheader("Key Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(
            f"**🏆 Best:** {top5.iloc[0]['Product Name']} "
            f"({top5.iloc[0]['Margin_Percent']:.1f}% margin)"
        )
    
    with col2:
        st.error(
            f"**📉 Worst:** {bottom5.iloc[0]['Product Name']} "
            f"({bottom5.iloc[0]['Margin_Percent']:.1f}% margin)"
        )
    
    # Combine for visualization 
    top_bott = pd.concat([bottom5, top5], ignore_index=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        top_bott,
        y='Product Name',
        x='Margin_Percent',
        orientation='h',
        title='Top 5 & Bottom 5 Products by Profit Margin',
        color='Margin_Percent',
        color_continuous_scale='RdYlGn',
        text_auto='.1f'
    )
    
    fig.update_layout(
        height=600,
        yaxis_title='Product',
        xaxis_title='Profit Margin (%)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data tables
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 5 Products")
        st.dataframe(
            top5[['Product Name', 'Margin_Percent']].style.format({
                'Margin_Percent': '{:.2f}%'
            }),
            hide_index=True
        )

    with col2:
        st.subheader("📉 Bottom 5 Products")
        st.dataframe(
            bottom5[['Product Name', 'Margin_Percent']].style.format({
                'Margin_Percent': '{:.2f}%'
            }),
            hide_index=True
        )

# QUESTION 5: Monthly Trend
elif tab == "Monthly Trend":
    st.title("Monthly Sales Trend")
    st.markdown("---")
    
    # Create month column
    df['Month'] = df['Order Date'].dt.to_period('M')
    
    # Aggregate by month
    monthly = df.groupby('Month').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    monthly['Month'] = monthly['Month'].astype(str)
    
    # Find peak month
    peak_month = monthly.loc[monthly['Sales'].idxmax()]
    
    # Display insight
    st.subheader("Key Insight")
    st.info(
        f"**Peak Sales Month:** {peak_month['Month']} "
        f"(${peak_month['Sales']:,.2f})"
    )
    
    st.write("""
    **Observation:** Sales typically spike in **November** (Black Friday effect),
    but drop in **December**, this is unusual for retail. This suggests a B2B business
    where companies reduce purchases during holiday shutdowns/vacations.\n\n**Potential Strategy:** Leading up to November, when sales are strong, ensure inventory is built with high margin items.
    December shows a B2B holiday shutdown pattern, create promotions targeting B2B companies and budgets i.e. bulk buying discounts. We may also be able to capitalize on post holiday recovery, feature newer attractive products during this time. 
    """)
    
    # Create line chart
    fig5 = px.line(
        monthly,
        x='Month',
        y='Sales',
        title='Monthly Sales Trend',
        markers=True
    )
    
    fig5.update_layout(
        height=400,
        xaxis_title='Month',
        yaxis_title='Sales ($)'
    )
    
    st.plotly_chart(fig5, use_container_width=True)

    # Show data table
    with st.expander("View Monthly Data"):
        st.dataframe(
            monthly.style.format({
                'Sales': '${:,.2f}',
                'Profit': '${:,.2f}'
            }),
            hide_index=True
        )

# FOOTER
st.sidebar.markdown("---")
st.sidebar.caption(
    "Built with Streamlit | Portfolio Project 2024"
)


