# Readiness Dimensions and Scoring Rubric

Score each dimension from 1 (not ready) to 5 (fully ready). Use half-points when a business falls clearly between two levels.

## 1. Data Maturity (Weight: 25%)

Evaluates the state of the organization's data assets, infrastructure, and governance.

**Score 1 - Ad Hoc / Non-Existent**:
- Data lives in spreadsheets, email threads, and individual hard drives
- No central database or data warehouse
- No data dictionary or schema documentation
- Duplicate and conflicting records are common
- No awareness of data quality issues

**Score 2 - Emerging**:
- Some structured data exists in databases or SaaS platforms
- No formal data governance or ownership
- Data quality is inconsistent; manual cleanup is frequent
- Limited ability to join data across systems
- Basic reporting exists but is unreliable

**Score 3 - Defined**:
- Central data store exists (data warehouse, lake, or consolidated database)
- Data ownership is assigned to specific teams or individuals
- Basic data quality checks are in place
- Key business entities (customers, transactions, products) are well-defined
- Regular reporting is functional and trusted by stakeholders

**Score 4 - Managed**:
- Data pipelines are automated and monitored
- Data quality is measured with defined SLAs
- Master data management practices are in place
- Historical data is preserved and accessible for at least 2 years
- Data catalog or discovery tools are available
- PII and sensitive data are classified and handled appropriately

**Score 5 - Optimized**:
- Real-time or near-real-time data pipelines
- Comprehensive data lineage tracking
- Self-service data access for business users
- Advanced data quality frameworks with automated remediation
- Data is treated as a strategic asset with executive sponsorship
- Full compliance with relevant regulations (GDPR, CCPA, HIPAA, etc.)

**Key Questions to Ask**:
- Where does your most important business data live today?
- How do you currently ensure data accuracy?
- Can you easily combine data from different systems?
- How far back does your historical data go?
- Who is responsible for data quality in your organization?
- Do you have documented data schemas or dictionaries?
- What percentage of your business data is digitized vs. paper/manual?
- How do you handle personally identifiable information (PII)?

## 2. Technology Stack (Weight: 20%)

Evaluates the current technical infrastructure and its compatibility with AI workloads.

**Score 1 - Legacy / Disconnected**:
- Core systems are 10+ years old with no API access
- On-premise only with no cloud presence
- No version control or CI/CD pipelines
- Manual deployments and server management
- Vendor lock-in with no export capabilities

**Score 2 - Basic**:
- Mix of legacy and modern systems
- Some cloud services (email, file storage) but core operations remain on-premise
- Limited API availability across systems
- Basic version control exists but is not universally adopted
- Some automation scripts but no formal DevOps practice

**Score 3 - Modern Foundation**:
- Cloud-first or hybrid infrastructure
- RESTful APIs available for core business systems
- Version control (Git) is standard practice
- CI/CD pipelines exist for key applications
- Containerization (Docker) is used for some workloads
- Monitoring and logging are in place

**Score 4 - AI-Compatible**:
- Cloud infrastructure with scalable compute (GPU access available or easily provisioned)
- Microservices architecture enabling modular AI integration
- API gateway managing internal and external integrations
- Infrastructure as code (Terraform, Pulumi, CloudFormation)
- Feature flags and A/B testing infrastructure
- Event-driven architecture supporting real-time processing

**Score 5 - AI-Native**:
- ML platform or MLOps infrastructure in place
- Model registry and experiment tracking
- Automated model training, evaluation, and deployment pipelines
- Edge computing capabilities for low-latency inference
- GPU/TPU clusters or serverless ML compute
- Comprehensive observability including model performance monitoring

**Key Questions to Ask**:
- What are your core business systems (ERP, CRM, etc.) and how old are they?
- Do your systems expose APIs for integration?
- What is your cloud strategy (on-prem, hybrid, cloud-native)?
- Do you use version control and CI/CD?
- Can you provision compute resources (including GPUs) on demand?
- What is your current approach to system integration?
- Do you have any existing ML/AI infrastructure?
- How do you handle system monitoring and logging?

## 3. Team Skills and Capacity (Weight: 20%)

Evaluates the human capital available for AI initiatives.

**Score 1 - No Technical Depth**:
- No in-house developers or data professionals
- All technology is managed by external vendors
- Staff has minimal digital literacy beyond basic office tools
- No understanding of AI concepts at any level of the organization
- Resistance to learning new tools is prevalent

**Score 2 - Basic Technical Team**:
- Small IT team focused on support and maintenance
- Some staff comfortable with data analysis in Excel or Google Sheets
- No data engineering, data science, or ML expertise
- Limited software development capability
- Awareness of AI exists but understanding is superficial

**Score 3 - Developing Capabilities**:
- Developers on staff with modern language proficiency (Python, JavaScript, etc.)
- At least one person with data analysis or data engineering skills
- Team members have completed AI/ML courses or certifications
- Management has a conceptual understanding of AI capabilities and limitations
- Willingness to invest in upskilling is demonstrated

**Score 4 - Strong Foundation**:
- Dedicated data team (analysts, engineers, or scientists)
- Developers experienced with API integrations and cloud services
- At least one person with hands-on ML/AI experience
- Cross-functional collaboration between technical and business teams
- Active learning culture with regular knowledge sharing
- Executive sponsor who understands AI ROI frameworks

**Score 5 - AI-Ready Team**:
- Data science or ML engineering team in place
- Full-stack capability from data engineering to model deployment
- Product managers experienced with AI product development
- Organization-wide AI literacy program completed
- Established partnerships with AI vendors or consultants
- Clear career paths for AI/ML roles

**Key Questions to Ask**:
- What does your technical team look like today?
- Do you have anyone with data science or ML experience?
- What programming languages does your team use?
- Have team members pursued AI/ML training or certifications?
- How does your leadership team view AI adoption?
- Is there budget allocated for training and upskilling?
- Do you work with external technology partners or consultants?
- How do technical and business teams collaborate today?

## 4. Process Documentation (Weight: 15%)

Evaluates how well business processes are understood, documented, and standardized.

**Score 1 - Tribal Knowledge**:
- Processes exist only in people's heads
- No standard operating procedures (SOPs)
- Outcomes vary significantly by who performs the task
- Key person dependencies are critical risks
- No process maps or workflow documentation

**Score 2 - Partially Documented**:
- Some processes are written down but documents are outdated
- Documentation exists in scattered locations (wikis, shared drives, emails)
- Processes are followed inconsistently across teams
- Onboarding relies heavily on shadowing and verbal instruction
- No regular review or update cycle for documentation

**Score 3 - Standardized**:
- Core business processes are documented with SOPs
- Documentation is centralized and accessible
- Process owners are identified
- Workflows are generally consistent across teams
- Regular review cycle exists (at least annually)
- Decision criteria are documented for common scenarios

**Score 4 - Measured and Managed**:
- Processes have defined KPIs and success metrics
- Workflow tools (BPM software, project management platforms) enforce process compliance
- Exception handling procedures are documented
- Process performance is tracked and reported
- Continuous improvement is practiced (lean, six sigma, or similar)
- Clear escalation paths are defined

**Score 5 - Optimized for Automation**:
- Processes are mapped with decision trees and logic flows
- Input/output specifications are defined for each process step
- Edge cases and exceptions are cataloged
- Processes are designed with automation in mind
- Business rules are externalized and configurable
- Process mining or task mining has been conducted

**Key Questions to Ask**:
- Are your core business processes documented?
- Where does process documentation live?
- How often is documentation reviewed and updated?
- Are processes followed consistently across teams and locations?
- Do you measure process performance with specific KPIs?
- What happens when a key employee leaves - how is knowledge transferred?
- Have you identified which processes are candidates for automation?
- Do you use any workflow or BPM tools?

## 5. Budget and Resources (Weight: 10%)

Evaluates the financial commitment and resource allocation for AI initiatives.

**Score 1 - No Allocation**:
- No budget earmarked for AI or advanced technology initiatives
- Technology spending is purely maintenance-focused
- No executive awareness of AI investment requirements
- Cost-cutting mentality dominates technology decisions
- No willingness to explore AI-related expenditures

**Score 2 - Exploratory**:
- Small discretionary budget could be redirected to AI exploration
- Leadership is open to hearing about AI but has not committed funds
- Technology budget covers current operations with minimal surplus
- ROI expectations are unclear or unrealistic (expecting immediate returns)
- No dedicated headcount for AI initiatives

**Score 3 - Committed**:
- Specific budget allocated for AI pilot projects
- Understanding that AI requires sustained investment over 12-18 months
- Willingness to hire or contract AI-specific talent
- Executive sponsorship with defined success criteria
- Budget covers tools, infrastructure, and training
- Total AI budget is at least 5-10% of annual technology spend

**Score 4 - Strategic Investment**:
- Multi-year AI budget with phased milestones
- Dedicated team or department for AI initiatives
- Budget includes ongoing model maintenance and monitoring costs
- Investment in change management and organizational adoption
- Clear ROI framework with realistic payback expectations (12-24 months)
- Contingency budget for iteration and pivots

**Score 5 - Fully Resourced**:
- AI is a board-level strategic priority with protected funding
- Comprehensive budget covering build, buy, and partner options
- Investment in research and innovation beyond immediate ROI
- Dedicated AI center of excellence with full staffing
- Budget for external partnerships, vendor evaluations, and conferences
- Ongoing operational budget for model retraining and data maintenance

**Key Questions to Ask**:
- Is there a specific budget allocated for AI initiatives?
- What is your overall annual technology spend?
- What ROI timeline are stakeholders expecting?
- Are you prepared to invest in a 12-18 month pilot before seeing significant returns?
- Is there budget for hiring or contracting specialized AI talent?
- Who controls the AI budget and what is the approval process?
- Have you factored in ongoing costs (infrastructure, maintenance, monitoring)?
- Is there executive sponsorship with decision-making authority?

## 6. Organizational Culture (Weight: 10%)

Evaluates the cultural readiness for AI-driven transformation.

**Score 1 - Resistant**:
- Strong resistance to change at all levels
- "We've always done it this way" mentality prevails
- Fear of job displacement dominates AI conversations
- No culture of experimentation or learning from failure
- Siloed departments with minimal cross-functional collaboration
- Distrust of technology-driven decisions

**Score 2 - Cautious**:
- Leadership acknowledges the need for change but has not acted
- Some curiosity about AI among individual contributors
- Change management is not a practiced discipline
- Past technology implementations have been painful or failed
- Limited transparency about organizational direction
- Innovation is discussed but not rewarded or resourced

**Score 3 - Open**:
- Leadership actively communicates the AI vision and rationale
- Employees are generally open to new tools and processes
- Some experience with successful technology-driven change
- Cross-functional teams exist and collaborate on projects
- Failure is tolerated in controlled experiments
- Regular communication about technology strategy

**Score 4 - Embracing**:
- Culture of continuous improvement and innovation
- Data-driven decision-making is the norm, not the exception
- Employees proactively suggest process improvements
- Change management is a core organizational competency
- Psychological safety exists for raising concerns about AI
- Internal AI champions advocate across departments
- Regular innovation sprints or hackathons

**Score 5 - AI-First Culture**:
- AI is embedded in the organizational identity and strategy
- Every department actively looks for AI opportunities
- Ethical AI principles are defined and followed
- Employees view AI as an augmentation tool, not a threat
- Learning and experimentation are rewarded in performance reviews
- External thought leadership on AI in the industry
- Structured feedback loops between AI users and developers

**Key Questions to Ask**:
- How does your organization typically react to new technology?
- Have past technology rollouts been successful? What went wrong or right?
- Is there anxiety about AI replacing jobs?
- How do teams collaborate across departments?
- Does leadership model data-driven decision-making?
- Is there a culture of experimentation and learning from failure?
- How is change typically communicated and managed?
- Do employees have a voice in technology adoption decisions?
