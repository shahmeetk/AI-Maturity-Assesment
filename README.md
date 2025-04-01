# AI Maturity Assessment Tool 🚀

A comprehensive tool for assessing an organization's AI maturity across different domains and phases. Built with Streamlit, this tool provides an interactive interface for conducting assessments and generating detailed reports.

## Features 🌟

- **Comprehensive Assessment Framework**: Evaluate AI maturity across multiple domains:
  - Business Domains (AI Discovery, Strategy & Governance, Cost Management)
  - Process Domains (Infrastructure, Model Development, MLOps, Compliance, Ethical AI)
  - Tools & Technology (Performance Optimization, Automation & Monitoring)

- **Multi-Phase Evaluation**: Assessment across three key phases:
  - Plan & Design
  - Implement
  - Operate & Improve

- **Maturity Levels**: Five-level maturity scale:
  1. Adhoc (Level 1)
  2. Repeatable (Level 2)
  3. Defined (Level 3)
  4. Optimized (Level 4)
  5. Innovative (Level 5)

- **Interactive UI**: User-friendly interface with:
  - Progress tracking
  - Dynamic form validation
  - Interactive charts and visualizations

- **Comprehensive Reporting**:
  - Detailed Excel reports
  - Visual dashboards
  - Domain-wise analysis
  - Category-level insights

## Local Setup 🛠️

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AI-Maturity-Assessment.git
   cd AI-Maturity-Assessment
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv aimaturity_env
   ```

3. **Activate Virtual Environment**
   - Windows:
     ```bash
     .\aimaturity_env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source aimaturity_env/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Streamlit Cloud Deployment ☁️

1. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Deploy directly from the repository
4. No additional configuration needed - Streamlit Cloud will use requirements.txt

## Enterprise Benefits 💼

1. **Strategic Planning**
   - Identify AI maturity gaps
   - Prioritize improvement areas
   - Track progress over time

2. **Risk Management**
   - Assess compliance readiness
   - Evaluate ethical AI practices
   - Monitor governance frameworks

3. **Resource Optimization**
   - Understand resource allocation
   - Identify training needs
   - Optimize infrastructure investments

4. **Competitive Advantage**
   - Benchmark against industry standards
   - Identify innovation opportunities
   - Guide digital transformation

5. **Standardization**
   - Establish consistent assessment criteria
   - Create repeatable processes
   - Enable cross-department comparison

## Code Structure 📁

```
AI-Maturity-Assessment/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore rules
├── ai_maturity_framework_final.json  # Assessment framework
└── ISSI_logo.png         # Logo file
```

## Session State Management 🔄

The application uses Streamlit's session state to manage:
- Assessment progress
- User inputs
- Navigation state
- Results storage

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please contact [your-email@domain.com]

## Authors
- Meet Shah


## Version History
- v1.0.0 (2024-03): Initial release
  - Basic assessment functionality
  - Excel report generation
  - Interactive charts and visualizations 