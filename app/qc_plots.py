# qc_plots.py
import plotly.graph_objects as go
import plotly.utils
import json
import traceback
from datetime import datetime, timedelta
from flask import jsonify, request, Blueprint

# Import from models - NO MODEL DEFINITIONS HERE
from models import db, QCData

# Create a blueprint for QC routes
qc_bp = Blueprint('qc', __name__, url_prefix='/api')

def create_levey_jennings_plot(dates, values, target_mean, target_sd, test_id, reagent_lot_id, qc_level):
    """
    Create a Levey-Jennings quality control plot
    """
    # Calculate control limits
    mean_line = target_mean
    plus_1sd = target_mean + target_sd
    minus_1sd = target_mean - target_sd
    plus_2sd = target_mean + (2 * target_sd)
    minus_2sd = target_mean - (2 * target_sd)
    plus_3sd = target_mean + (3 * target_sd)
    minus_3sd = target_mean - (3 * target_sd)
    
    # Determine point colors based on control rules
    colors = []
    for value in values:
        if value > plus_3sd or value < minus_3sd:
            colors.append('red')  # Out of control (>3SD)
        elif value > plus_2sd or value < minus_2sd:
            colors.append('orange')  # Warning (>2SD)
        else:
            colors.append('blue')  # In control
    
    # Create the plot
    fig = go.Figure()
    
    # Add data points
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='markers+lines',
        marker=dict(
            color=colors,
            size=8,
            line=dict(width=1, color='white')
        ),
        line=dict(color='lightblue', width=1),
        name='QC Values',
        hovertemplate='<b>Date:</b> %{x}<br><b>Value:</b> %{y:.3f}<extra></extra>'
    ))
    
    # Add control limit lines
    fig.add_hline(y=mean_line, line_dash="solid", line_color="green", line_width=2,
                  annotation_text="Mean", annotation_position="right")
    
    fig.add_hline(y=plus_1sd, line_dash="dash", line_color="blue", line_width=1,
                  annotation_text="+1SD", annotation_position="right")
    fig.add_hline(y=minus_1sd, line_dash="dash", line_color="blue", line_width=1,
                  annotation_text="-1SD", annotation_position="right")
    
    fig.add_hline(y=plus_2sd, line_dash="dash", line_color="orange", line_width=1,
                  annotation_text="+2SD", annotation_position="right")
    fig.add_hline(y=minus_2sd, line_dash="dash", line_color="orange", line_width=1,
                  annotation_text="-2SD", annotation_position="right")
    
    fig.add_hline(y=plus_3sd, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="+3SD", annotation_position="right")
    fig.add_hline(y=minus_3sd, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="-3SD", annotation_position="right")
    
    # Update layout
    fig.update_layout(
        title=f'Levey-Jennings Plot: {test_id} - {reagent_lot_id} ({qc_level})',
        xaxis_title='Date',
        yaxis_title='Measurement Value',
        hovermode='x unified',
        showlegend=True,
        template='plotly_white',
        height=500,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Style the plot for web display
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

@qc_bp.route('/levey-jennings-plot/<test_id>/<reagent_lot_id>/<qc_level>')
def levey_jennings_plot(test_id, reagent_lot_id, qc_level):
    """
    Flask route to generate Levey-Jennings plot data
    """
    try:
        # Get optional parameters
        days = request.args.get('days', 30, type=int)
        
        # Query the database
        measurements = QCData.query.filter_by(
            test_id=test_id,
            reagent_lot_id=reagent_lot_id,
            qc_level=qc_level
        ).filter(
            QCData.measurement_date >= datetime.utcnow() - timedelta(days=days)
        ).order_by(QCData.measurement_date).all()
        
        if not measurements:
            return jsonify({'error': 'No QC data found for the specified parameters'}), 404
        
        # Extract data for plotting
        dates = [m.measurement_date for m in measurements]
        values = [float(m.measurement_value) for m in measurements]
        target_mean = float(measurements[0].target_mean)
        target_sd = float(measurements[0].target_sd)
        
        # Create the plot
        fig = create_levey_jennings_plot(
            dates, values, target_mean, target_sd, 
            test_id, reagent_lot_id, qc_level
        )
        
        # Convert to JSON for frontend
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Return plot data and summary statistics
        return jsonify({
            'plot': plot_json,
            'summary': {
                'total_points': len(values),
                'mean': target_mean,
                'sd': target_sd,
                'out_of_control': sum(1 for v in values if abs(v - target_mean) > 3 * target_sd),
                'warning': sum(1 for v in values if 2 * target_sd < abs(v - target_mean) <= 3 * target_sd),
                'date_range': f"{min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}"
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating plot: {str(e)}'}), 500

@qc_bp.route('/qc-data/<test_id>/<reagent_lot_id>/<qc_level>')
def get_qc_data(test_id, reagent_lot_id, qc_level):
    try:
        days = request.args.get('days', 30, type=int)
        
        measurements = QCData.query.filter_by(
            test_id=test_id,
            reagent_lot_id=reagent_lot_id,
            qc_level=qc_level
        ).filter(
            QCData.measurement_date >= datetime.utcnow() - timedelta(days=days)
        ).order_by(QCData.measurement_date).all()
        
        return jsonify([m.to_dict() for m in measurements])
        
    except Exception as e:
        print(f"ERROR in get_qc_data: {str(e)}")
        return jsonify({'error': f'Error getting QC data: {str(e)}'}), 500

@qc_bp.route('/qc-summary/<test_id>')
def qc_summary(test_id):
    """
    Get summary of available QC data for a test
    """
    try:
        print(f"DEBUG: Trying to get QC summary for test_id: {test_id}")
        
        # Get unique combinations for this test
        combinations = db.session.query(
            QCData.reagent_lot_id,
            QCData.qc_level,
            db.func.count(QCData.qc_data_id).label('count'),
            db.func.max(QCData.measurement_date).label('latest_date')
        ).filter_by(test_id=test_id).group_by(
            QCData.reagent_lot_id,
            QCData.qc_level
        ).all()
        
        print(f"DEBUG: Found {len(combinations)} combinations")
        
        result = []
        for combo in combinations:
            result.append({
                'reagent_lot_id': combo.reagent_lot_id,
                'qc_level': combo.qc_level,
                'measurement_count': combo.count,
                'latest_measurement': combo.latest_date.strftime('%Y-%m-%d %H:%M') if combo.latest_date else None
            })
        
        print(f"DEBUG: Returning result: {result}")
        
        return jsonify({
            'test_id': test_id,
            'combinations': result
        })
        
    except Exception as e:
        print(f"ERROR in qc_summary: {str(e)}")
        print(f"ERROR traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Error getting QC summary: {str(e)}'}), 500