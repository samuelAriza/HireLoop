import dash
import uuid
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from django_plotly_dash import DjangoDash

from ..repositories.microservice_repository import MicroServiceRepository
from ..repositories.cart_repository import CartRepository
from ..services.analytics_service import MarketAnalyticsService

from microservices.models import MicroService
from mentorship_session.models import MentorshipSession

# Repositories and service
micro_repo = MicroServiceRepository()
cart_repo = CartRepository()
analytics_service = MarketAnalyticsService(micro_repo, cart_repo)

# Dash app
app = DjangoDash("MarketDashboard")

# Layout
app.layout = html.Div([
    html.H2("Market Analytics Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    dcc.Tabs(id="tabs", value="categories", children=[
        dcc.Tab(label="Categories", value="categories"),
        dcc.Tab(label="Prices", value="prices"),
        dcc.Tab(label="Freelancers", value="freelancers"),
        dcc.Tab(label="Delivery Time", value="delivery"),
        dcc.Tab(label="Popular Products", value="products"),
    ]),
    html.Div(id="tab-content", style={'margin': '20px'})
])

def safe_get_object_name(model_class, object_id, default_name="Unknown"):
    try:
        # Make sure object_id is a valid UUID
        if not isinstance(object_id, uuid.UUID):
            object_id = uuid.UUID(str(object_id))
        
        obj = model_class.objects.get(pk=object_id)
        
        if model_class == MicroService:
            return obj.title 
        elif model_class == MentorshipSession:
            return obj.topic
        else:
            return default_name
    except model_class.DoesNotExist:
        return f"{default_name} (ID: {object_id})"
    except Exception as e:
        return f"Error (ID: {object_id})"

# Callback
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    try:
        # Get updated data each time
        dashboard_data = analytics_service.get_dashboard_data()
        
        # DEBUG: Print all dashboard data
        print("=== DEBUG: DASHBOARD DATA ===")
        print(f"Complete dashboard data: {dashboard_data}")
        print("=" * 50)

        # -------------------- Categories --------------------
        if tab == "categories":
            category_data = dashboard_data["category_distribution"]["data"]
            print(f"DEBUG - Categories - Raw data: {category_data}")
            print(f"DEBUG - Categories - Data type: {type(category_data)}")
            print(f"DEBUG - Categories - Length: {len(category_data) if category_data else 0}")
            
            if not category_data:
                print("DEBUG - Categories - No data to show")
                return html.Div([
                    html.H3("Distribution by Categories"),
                    html.P("No category data to display.", 
                          style={'textAlign': 'center', 'color': 'gray'})
                ])
            
            df = pd.DataFrame(category_data)
            print(f"DEBUG - Categories - DataFrame created: {df}")
            print(f"DEBUG - Categories - DataFrame columns: {df.columns.tolist()}")
            
            fig = px.pie(
                df, 
                names="category", 
                values="count",
                title="Distribution of Microservices by Category",
                hole=0.3  # Donut chart
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return html.Div([
                dcc.Graph(figure=fig, style={'height': '500px'})
            ])

        # -------------------- Prices --------------------
        elif tab == "prices":
            price_data = dashboard_data["price_analysis"]["data"]
            print(f"DEBUG - Prices - Raw data: {price_data}")
            print(f"DEBUG - Prices - Data type: {type(price_data)}")
            print(f"DEBUG - Prices - Length: {len(price_data) if price_data else 0}")
            
            if not price_data:
                print("DEBUG - Prices - No data to show")
                return html.Div([
                    html.H3("Price Analysis"),
                    html.P("No price data to display.", 
                          style={'textAlign': 'center', 'color': 'gray'})
                ])
            
            df = pd.DataFrame(price_data)
            print(f"DEBUG - Prices - DataFrame created: {df}")
            print(f"DEBUG - Prices - DataFrame columns: {df.columns.tolist()}")
            
            # Bar chart for average prices
            fig1 = px.bar(
                df, 
                x="category", 
                y="avg_price",
                title="Average Price by Category",
                labels={'avg_price': 'Average Price ($)', 'category': 'Category'}
            )
            fig1.update_layout(xaxis_tickangle=-45)
            
            # Price range chart
            fig2 = go.Figure()
            for _, row in df.iterrows():
                fig2.add_trace(go.Scatter(
                    x=[row['category'], row['category']],
                    y=[row['min_price'], row['max_price']],
                    mode='lines+markers',
                    name=f"{row['category']} (range)",
                    line=dict(width=4),
                    marker=dict(size=8)
                ))
            
            fig2.update_layout(
                title="Price Range by Category",
                xaxis_title="Category",
                yaxis_title="Price ($)",
                xaxis_tickangle=-45
            )
            
            return html.Div([
                dcc.Graph(figure=fig1, style={'height': '400px'}),
                dcc.Graph(figure=fig2, style={'height': '400px'})
            ])

        # -------------------- Freelancers --------------------
        elif tab == "freelancers":
            freelancers_data = dashboard_data["top_freelancers"]["data"]
            print(f"DEBUG - Freelancers - Raw data: {freelancers_data}")
            print(f"DEBUG - Freelancers - Data type: {type(freelancers_data)}")
            print(f"DEBUG - Freelancers - Length: {len(freelancers_data) if freelancers_data else 0}")
            
            if not freelancers_data:
                print("DEBUG - Freelancers - No data to show")
                return html.Div([
                    html.H3("Top Freelancers"),
                    html.P("No freelancer data to display.", 
                          style={'textAlign': 'center', 'color': 'gray'})
                ])
            
            df = pd.DataFrame(freelancers_data)
            print(f"DEBUG - Freelancers - DataFrame created: {df}")
            print(f"DEBUG - Freelancers - DataFrame columns: {df.columns.tolist()}")
            
            fig = px.bar(
                df, 
                x="freelancer_id", 
                y="active_services",
                title="Top Freelancers by Active Services",
                labels={'active_services': 'Active Services', 'freelancer_id': 'Freelancer'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            return html.Div([
                dcc.Graph(figure=fig, style={'height': '500px'})
            ])

        # -------------------- Delivery Time --------------------
        elif tab == "delivery":
            delivery_stats = dashboard_data["delivery_time_stats"]
            general = delivery_stats["general"]
            by_category = delivery_stats["by_category"]
            
            print(f"DEBUG - Delivery - General stats: {general}")
            print(f"DEBUG - Delivery - By category: {by_category}")
            print(f"DEBUG - Delivery - General type: {type(general)}")
            print(f"DEBUG - Delivery - By category type: {type(by_category)}")
            print(f"DEBUG - Delivery - By category length: {len(by_category) if by_category else 0}")
            
            if not by_category:
                print("DEBUG - Delivery - No category data to show")
                fig = go.Figure()
                fig.add_annotation(
                    text="No delivery time data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=16)
                )
                fig.update_layout(
                    title="Average Delivery Time by Category",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False)
                )
            else:
                df = pd.DataFrame(by_category)
                print(f"DEBUG - Delivery - DataFrame created: {df}")
                print(f"DEBUG - Delivery - DataFrame columns: {df.columns.tolist()}")
                
                fig = px.bar(
                    df, 
                    x="name", 
                    y="avg_delivery_time",
                    title="Average Delivery Time by Category",
                    labels={'avg_delivery_time': 'Average days', 'name': 'Category'}
                )
                fig.update_layout(xaxis_tickangle=-45)
            
            stats_cards = html.Div([
                html.Div([
                    html.H4("📊 General Statistics", style={'textAlign': 'center'}),
                    html.Div([
                        html.Div([
                            html.H5("Average", style={'margin': '0', 'color': '#007bff'}),
                            html.P(f"{general.get('avg_days', 0)} days", 
                                  style={'fontSize': '24px', 'margin': '5px 0', 'fontWeight': 'bold'})
                        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'border-radius': '8px', 'margin': '5px'}),
                        
                        html.Div([
                            html.H5("Minimum", style={'margin': '0', 'color': '#28a745'}),
                            html.P(f"{general.get('min_days', 0)} days", 
                                  style={'fontSize': '24px', 'margin': '5px 0', 'fontWeight': 'bold'})
                        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'border-radius': '8px', 'margin': '5px'}),
                        
                        html.Div([
                            html.H5("Maximum", style={'margin': '0', 'color': '#dc3545'}),
                            html.P(f"{general.get('max_days', 0)} days", 
                                  style={'fontSize': '24px', 'margin': '5px 0', 'fontWeight': 'bold'})
                        ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'border-radius': '8px', 'margin': '5px'})
                    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'})
                ], style={'margin': '20px 0', 'padding': '20px', 'border': '1px solid #dee2e6', 'border-radius': '10px'})
            ])
            
            return html.Div([
                dcc.Graph(figure=fig, style={'height': '400px'}),
                stats_cards
            ])

        # -------------------- Popular Products --------------------
        elif tab == "products":
            popular_data = dashboard_data["popular_products"]
            micro_list = popular_data["microservices"]
            mentorships_list = popular_data["mentorships"]

            print(f"DEBUG - Products - Complete popular data: {popular_data}")
            print(f"DEBUG - Products - Microservices: {micro_list}")
            print(f"DEBUG - Products - Mentorships: {mentorships_list}")
            print(f"DEBUG - Products - Microservices type: {type(micro_list)}")
            print(f"DEBUG - Products - Mentorships type: {type(mentorships_list)}")
            print(f"DEBUG - Products - Microservices length: {len(micro_list) if micro_list else 0}")
            print(f"DEBUG - Products - Mentorships length: {len(mentorships_list) if mentorships_list else 0}")

            # Convert to DataFrame and map names
            micro_df = pd.DataFrame(micro_list) if micro_list else pd.DataFrame()
            mentorships_df = pd.DataFrame(mentorships_list) if mentorships_list else pd.DataFrame()

            print(f"DEBUG - Products - Microservices DataFrame: {micro_df}")
            print(f"DEBUG - Products - Mentorships DataFrame: {mentorships_df}")

            # Map object_id to name safely
            if not micro_df.empty:
                print(f"DEBUG - Products - Microservices columns: {micro_df.columns.tolist()}")
                micro_df['name'] = micro_df['object_id'].apply(
                    lambda id: safe_get_object_name(MicroService, id, "Microservice")
                )
                print(f"DEBUG - Products - Microservices DataFrame with names: {micro_df}")
                
            if not mentorships_df.empty:
                print(f"DEBUG - Products - Mentorships columns: {mentorships_df.columns.tolist()}")
                mentorships_df['name'] = mentorships_df['object_id'].apply(
                    lambda id: safe_get_object_name(MentorshipSession, id, "Mentorship")
                )
                print(f"DEBUG - Products - Mentorships DataFrame with names: {mentorships_df}")

            # Create figures
            if micro_df.empty:
                print("DEBUG - Products - No microservices to show")
                fig1 = go.Figure()
                fig1.add_annotation(
                    text="No microservices added to cart",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=14)
                )
                fig1.update_layout(
                    title="Most Added Microservices to Cart",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    height=300
                )
            else:
                # Limit to top 10 and sort
                micro_df = micro_df.nlargest(10, 'times_added')
                print(f"DEBUG - Products - Top 10 microservices: {micro_df}")
                fig1 = px.bar(
                    micro_df, 
                    x='times_added', 
                    y='name', 
                    orientation='h',
                    title="Top 10 Most Added Microservices to Cart",
                    labels={'times_added': 'Times Added', 'name': 'Microservice'}
                )

            if mentorships_df.empty:
                print("DEBUG - Products - No mentorships to show")
                fig2 = go.Figure()
                fig2.add_annotation(
                    text="No mentorships added to cart",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=14)
                )
                fig2.update_layout(
                    title="Most Added Mentorships to Cart",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    height=300
                )
            else:
                # Limit to top 10 and sort
                mentorships_df = mentorships_df.nlargest(10, 'times_added')
                print(f"DEBUG - Products - Top 10 mentorships: {mentorships_df}")
                fig2 = px.bar(
                    mentorships_df, 
                    x='times_added', 
                    y='name', 
                    orientation='h',
                    title="Top 10 Most Added Mentorships to Cart",
                    labels={'times_added': 'Times Added', 'name': 'Mentorship'}
                )

            return html.Div([
                dcc.Graph(figure=fig1, style={'height': '400px'}),
                html.Hr(),
                dcc.Graph(figure=fig2, style={'height': '400px'})
            ])

        # Default tab
        print("DEBUG - Default tab selected")
        return html.Div([
            html.H3("Welcome to the Dashboard"),
            html.P("Select a tab to view marketplace analytics.", 
                  style={'textAlign': 'center', 'fontSize': '16px', 'color': 'gray'})
        ])
        
    except Exception as e:
        # Global error handling with more information
        print(f"DEBUG - GLOBAL ERROR: {str(e)}")
        print(f"DEBUG - ERROR TYPE: {type(e)}")
        import traceback
        print(f"DEBUG - TRACEBACK: {traceback.format_exc()}")
        
        return html.Div([
            html.H3("Error loading data", style={'color': 'red'}),
            html.P(f"An error occurred: {str(e)}", style={'color': 'red'}),
            html.P("Please check the database configuration and repositories."),
            html.P(f"Error type: {type(e).__name__}", style={'fontSize': '12px', 'color': 'gray'})
        ])