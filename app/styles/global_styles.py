def load_global_styles():
    return """
    <style>
        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: #0B0F17;
            color: #F9FAFB;
        }

        [data-testid="stHeader"] {
            background: #0B0F17;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 42px;
            padding-bottom: 36px;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        .app-title {
            font-size: 30px;
            font-weight: 850;
            color: #F9FAFB;
            margin-bottom: 8px;
            line-height: 1.15;
        }

        .app-subtitle {
            font-size: 15px;
            color: #CBD5E1;
            margin-bottom: 18px;
            max-width: 760px;
            line-height: 1.5;
            word-break: normal;
            overflow-wrap: normal;
            hyphens: none;
        }

        .section-title {
            font-size: 15px;
            font-weight: 800;
            color: #F9FAFB;
            margin-top: 0;
            margin-bottom: 6px;
        }

        .section-caption {
            color: #94A3B8;
            font-size: 12px;
            line-height: 1.45;
            margin-bottom: 8px;
        }

        .system-strip {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 8px;
            margin: 0 0 14px 0;
        }

        .system-step {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 8px 10px;
            min-width: 0;
            min-height: 48px;
        }

        .system-step-label {
            color: #F9FAFB;
            font-size: 12px;
            font-weight: 800;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .system-step-owner {
            color: #94A3B8;
            font-size: 10px;
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 8px;
        }

        .orchestration-strip {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }

        .orchestration-chip {
            background: #0B1220;
            border: 1px solid #243244;
            border-radius: 999px;
            color: #CBD5E1;
            font-size: 11px;
            font-weight: 750;
            padding: 5px 9px;
            white-space: nowrap;
        }

        .orchestration-chip strong {
            color: #60A5FA;
        }

        .summary-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 8px 10px;
            min-width: 0;
        }

        .summary-label {
            color: #94A3B8;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
        }

        .summary-value {
            color: #F9FAFB;
            font-size: 13px;
            font-weight: 850;
            margin-top: 3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .summary-value.risk-low {
            color: #4ADE80;
        }

        .summary-value.risk-medium {
            color: #FBBF24;
        }

        .summary-value.risk-high {
            color: #F87171;
        }

        .response-card {
            background: #F8FAFC;
            color: #111827;
            padding: 12px 14px;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
            font-size: 13px;
            line-height: 1.45;
            width: 100%;
            max-height: 150px;
            overflow-y: auto;
        }

        .empty-response {
            background: #111827;
            border: 1px dashed #334155;
            border-radius: 8px;
            color: #94A3B8;
            padding: 12px 14px;
            font-size: 13px;
            line-height: 1.45;
        }

        .timeline {
            display: grid;
            gap: 7px;
            margin-top: 10px;
        }

        .timeline-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 8px 10px;
        }

        .timeline-step {
            color: #F9FAFB;
            font-size: 12px;
            font-weight: 850;
        }

        .timeline-detail {
            color: #94A3B8;
            font-size: 11px;
            line-height: 1.4;
            margin-top: 2px;
        }

        .guardrail-list {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-top: 8px;
        }

        .guardrail-item {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            color: #CBD5E1;
            font-size: 12px;
            line-height: 1.35;
            padding: 9px 10px;
        }

        .guardrail-item strong {
            color: #F9FAFB;
        }

        .detail-section {
            margin-top: 20px;
        }

        .detail-card {
            background: #0F172A;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 14px 16px;
        }

        .reason-box {
            background: #111827;
            border-left: 3px solid #60A5FA;
            color: #CBD5E1;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 12px;
            line-height: 1.45;
            margin-bottom: 8px;
        }

        .metric-card {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 14px 16px;
            color: #E5E7EB;
        }

        .metric-label {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .metric-value {
            color: #F9FAFB;
            font-size: 16px;
            font-weight: 850;
            margin-top: 4px;
        }

        div.stButton > button {
            height: 40px;
            font-size: 15px;
            font-weight: 750;
            border-radius: 8px;
            background: #2563EB;
            border: none;
        }

        div.stButton > button:hover {
            background: #1D4ED8;
            border: none;
        }

        textarea {
            font-size: 13px !important;
            background: #1F2430 !important;
            color: #F9FAFB !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 8px;
            border-color: #243244;
            background: #0F172A;
        }

        div[data-testid="stExpander"] {
            border-color: #243244;
            background: #0F172A;
            border-radius: 8px;
        }

        div[data-baseweb="select"] > div {
            background: #1F2430;
            border-color: #243244;
            color: #F9FAFB;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 14px 16px;
        }

        div[data-testid="stSelectbox"] {
            margin-bottom: 4px;
        }
    </style>
    """
