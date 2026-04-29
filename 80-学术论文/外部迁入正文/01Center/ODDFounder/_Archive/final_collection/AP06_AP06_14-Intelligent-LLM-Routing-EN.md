# CostLLM: An Intelligent Routing Framework for Cost-Optimized LLM Model Selection

**Authors**: [Author Name]  
**Affiliation**: [Institution]  
**Date**: January 2026  
**Keywords**: LLM Routing, Cost Optimization, Task Complexity, Model Selection, Multi-Model Orchestration

---

## Abstract

As organizations deploy multiple Large Language Models (LLMs) with varying capabilities and costs, a critical challenge emerges: **how to automatically select the optimal model for each task**. Using expensive models like Advanced Model for simple queries wastes 50-90% of costs, while using cheap models for complex tasks leads to quality degradation and costly retries. This paper introduces **CostLLM**, an intelligent routing framework that automatically evaluates task complexity and selects the cost-optimal model. Our key contributions include: (1) a **Dual-Layer Evaluation Architecture** combining zero-cost Fast Eval (<5ms) with precise LLM-based assessment, (2) a **Multi-Factor Complexity Scoring** algorithm considering message patterns, keywords, domain, and historical data, (3) a **Self-Learning Feedback Loop** that continuously improves routing decisions, and (4) a **Cost-Aware Circuit Breaker** preventing budget overruns. Deployed on the WizAxis platform, CostLLM achieves 67% cost reduction while maintaining 96% quality parity with always-using-best-model baseline.

---

## 1. Introduction

### 1.1 The Model Selection Dilemma

The LLM landscape has exploded with options: Advanced Model Turbo ($0.01/1K input), Claude-3 Advanced Model ($0.015/1K), Basic Model Turbo ($0.0005/1K), Intermediate Model ($0.0001/1K). Each model offers different trade-offs between capability, latency, and cost.

**The naive approaches fail**:
- **Always use the best model**: Wastes 50-90% of budget on simple tasks
- **Always use the cheapest model**: Quality suffers, retry costs accumulate
- **Manual task classification**: Doesn't scale, prone to human error

Consider these real scenarios:

| Task | Optimal Model | Cost if Advanced Model | Cost if Optimal | Savings |
|------|---------------|---------------|-----------------|---------|
| "What is 2+2?" | Intermediate Model | $0.01 | $0.0001 | 99% |
| "Translate 'hello' to French" | Basic Model | $0.01 | $0.0005 | 95% |
| "Design a microservices architecture" | Advanced Model | $0.03 | $0.03 | 0% |
| "Debug this complex async code" | Claude-3.5 | $0.01 | $0.003 | 70% |

**The core insight**: Task complexity varies dramatically, but model selection is often static.

### 1.2 Research Questions

This paper addresses three key questions:

1. **How to evaluate task complexity automatically** without expensive LLM calls?
2. **How to map complexity to optimal model selection** considering cost, quality, and latency?
3. **How to continuously improve routing decisions** through feedback?

### 1.3 Contributions

1. **Dual-Layer Evaluation**: Fast Eval (zero-cost, <5ms) + Precise Eval (LLM-based, ~$0.001)
2. **Multi-Factor Complexity Algorithm**: Combining 5 factors with learned weights
3. **Self-Learning Loop**: Continuous improvement from user feedback and outcomes
4. **Production System**: Deployed on WizAxis serving 1,200+ daily users

---

## 2. Related Work

### 2.1 LLM Routing Systems

**LiteLLM** provides unified API access to multiple models but relies on static routing rules. **OpenRouter** offers model selection but without automatic complexity assessment. **Martian** introduced routing based on task type but requires manual classification.

### 2.2 Cost Optimization Approaches

**Prompt Caching** (Anthropic, 2024) reduces costs for repeated system prompts. **Semantic Caching** stores similar query results. These are complementary to routing—they reduce costs for repeated queries, while routing optimizes model selection for new queries.

### 2.3 Task Complexity Assessment

Prior work on task complexity focuses on educational contexts (Bloom's Taxonomy) or software engineering (cyclomatic complexity). **FrugalGPT** (Chen et al., 2023) proposed cascading LLM calls but adds latency. Our approach differs by **predicting complexity before any LLM call**.

---

## 3. System Architecture

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CostLLM Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Request ──▶ ┌──────────────┐                                  │
│               │  Fast Eval   │ ◀── Zero Cost, <5ms              │
│               │  (Rule-based)│                                  │
│               └──────┬───────┘                                  │
│                      │                                          │
│           ┌──────────┴──────────┐                               │
│           │                     │                               │
│    confidence ≥ 70%      confidence < 70%                       │
│           │                     │                               │
│           ▼                     ▼                               │
│   ┌──────────────┐    ┌──────────────────┐                     │
│   │Direct Route  │    │   Precise Eval   │ ◀── ~$0.001/call    │
│   │              │    │   (LLM-based)    │                     │
│   └──────┬───────┘    └────────┬─────────┘                     │
│          │                     │                               │
│          └──────────┬──────────┘                               │
│                     ▼                                          │
│          ┌──────────────────┐                                  │
│          │  Model Selector  │                                  │
│          │  (Cost × Quality)│                                  │
│          └────────┬─────────┘                                  │
│                   ▼                                            │
│          ┌──────────────────┐                                  │
│          │   LLM Provider   │                                  │
│          │  (via LiteLLM)   │                                  │
│          └────────┬─────────┘                                  │
│                   ▼                                            │
│          ┌──────────────────┐                                  │
│          │ Feedback Loop    │ ◀── Quality signals              │
│          │ (Self-Learning)  │                                  │
│          └──────────────────┘                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Design Principles

1. **Zero-Cost First**: Avoid LLM calls for complexity assessment when possible
2. **Fail-Safe Defaults**: When uncertain, prefer quality over cost savings
3. **Continuous Learning**: Every request improves future routing
4. **Transparency**: Routing decisions are explainable and auditable

---

## 4. Dual-Layer Complexity Evaluation

### 4.1 Fast Eval: Zero-Cost Assessment

Fast Eval uses rule-based heuristics to estimate complexity without any LLM call:

```python
class FastEval:
    """
    Zero-cost complexity evaluation.
    Latency: <5ms
    """
    
    def evaluate(self, request: Request) -> EvalResult:
        scores = []
        confidences = []
        
        # Factor 1: Message count (weight: 0.15)
        msg_score, msg_conf = self._eval_message_count(request.messages)
        scores.append(msg_score * 0.15)
        confidences.append(msg_conf)
        
        # Factor 2: Message length (weight: 0.20)
        len_score, len_conf = self._eval_message_length(request.messages)
        scores.append(len_score * 0.20)
        confidences.append(len_conf)
        
        # Factor 3: Keyword hints (weight: 0.30)
        kw_score, kw_conf = self._eval_keywords(request.messages)
        scores.append(kw_score * 0.30)
        confidences.append(kw_conf)
        
        # Factor 4: Historical similarity (weight: 0.20)
        hist_score, hist_conf = self._eval_historical(request)
        scores.append(hist_score * 0.20)
        confidences.append(hist_conf)
        
        # Factor 5: Domain detection (weight: 0.15)
        dom_score, dom_conf = self._eval_domain(request.messages)
        scores.append(dom_score * 0.15)
        confidences.append(dom_conf)
        
        complexity = sum(scores)
        confidence = self._aggregate_confidence(confidences)
        
        return EvalResult(
            complexity_score=complexity,
            confidence=confidence,
            recommended_model=self._map_to_model(complexity),
            reasoning=self._generate_reasoning(scores)
        )
```

### 4.2 Factor Details

#### Factor 1: Message Count
```python
def _eval_message_count(self, messages: List[Message]) -> Tuple[float, float]:
    count = len(messages)
    
    if count <= 2:
        return 2.0, 0.9   # Simple, high confidence
    elif count <= 5:
        return 4.0, 0.8
    elif count <= 10:
        return 6.0, 0.7
    else:
        return 8.0, 0.6   # Complex, lower confidence
```

#### Factor 2: Message Length
```python
def _eval_message_length(self, messages: List[Message]) -> Tuple[float, float]:
    avg_length = sum(len(m.content) for m in messages) / len(messages)
    
    if avg_length < 100:
        return 2.0, 0.85
    elif avg_length < 500:
        return 4.0, 0.80
    elif avg_length < 2000:
        return 6.0, 0.70
    else:
        return 8.0, 0.60
```

#### Factor 3: Keyword Hints
```python
KEYWORD_CATEGORIES = {
    "simple": {
        "keywords": ["translate", "summarize", "what is", "define", "list"],
        "complexity": 2.0,
        "confidence": 0.85
    },
    "medium": {
        "keywords": ["analyze", "compare", "explain why", "how does"],
        "complexity": 5.0,
        "confidence": 0.75
    },
    "complex": {
        "keywords": ["design", "architect", "optimize", "debug", "implement"],
        "complexity": 7.0,
        "confidence": 0.70
    },
    "expert": {
        "keywords": ["prove", "derive", "complex algorithm", "distributed system"],
        "complexity": 9.0,
        "confidence": 0.65
    }
}
```

#### Factor 4: Historical Similarity
```python
def _eval_historical(self, request: Request) -> Tuple[float, float]:
    """
    Find similar past requests and use their actual complexity.
    """
    similar = self.history_store.find_similar(
        request.messages,
        threshold=0.85,
        limit=5
    )
    
    if not similar:
        return 5.0, 0.3  # Default, low confidence
    
    avg_complexity = sum(s.actual_complexity for s in similar) / len(similar)
    confidence = min(0.9, 0.5 + len(similar) * 0.1)
    
    return avg_complexity, confidence
```

#### Factor 5: Domain Detection
```python
DOMAIN_COMPLEXITY = {
    "general_qa": 3.0,
    "translation": 2.0,
    "summarization": 3.0,
    "code_generation": 6.0,
    "code_review": 7.0,
    "math_reasoning": 7.0,
    "creative_writing": 5.0,
    "data_analysis": 6.0,
    "system_design": 8.0
}
```

### 4.3 Precise Eval: LLM-Based Assessment

When Fast Eval confidence is below 70%, we invoke Precise Eval:

```python
class PreciseEval:
    """
    LLM-based complexity evaluation.
    Cost: ~$0.001 per call
    Latency: ~200ms
    """
    
    EVAL_PROMPT = """
    Analyze the following task and rate its complexity from 1-10:
    
    Task:
    {messages}
    
    Consider:
    1. Reasoning depth required
    2. Domain expertise needed
    3. Output length/structure complexity
    4. Ambiguity level
    
    Respond in JSON:
    {
        "complexity": <1-10>,
        "recommended_tier": "basic|standard|advanced|expert",
        "reasoning": "<brief explanation>"
    }
    """
    
    def evaluate(self, request: Request) -> EvalResult:
        # Use cheap, fast model for evaluation
        response = self.llm.call(
            model="Basic Model-turbo",
            messages=[{
                "role": "user",
                "content": self.EVAL_PROMPT.format(
                    messages=self._format_messages(request.messages)
                )
            }],
            max_tokens=150,
            temperature=0
        )
        
        result = json.loads(response.content)
        
        return EvalResult(
            complexity_score=result["complexity"],
            confidence=0.90,  # LLM assessment is high confidence
            recommended_model=self._tier_to_model(result["recommended_tier"]),
            reasoning=result["reasoning"]
        )
```

### 4.4 Evaluation Decision Flow

```python
def evaluate_complexity(request: Request) -> EvalResult:
    # Step 1: Fast Eval (always)
    fast_result = fast_eval.evaluate(request)
    
    # Step 2: Check confidence
    if fast_result.confidence >= 0.70:
        return fast_result
    
    # Step 3: Check if precise eval is cost-effective
    estimated_savings = calculate_potential_savings(request, fast_result)
    precise_eval_cost = 0.001  # ~$0.001 per call
    
    if estimated_savings < precise_eval_cost * 2:
        # Not worth the precise eval cost
        return fast_result
    
    # Step 4: Precise Eval
    precise_result = precise_eval.evaluate(request)
    
    # Step 5: Cache for future similar requests
    history_store.record(request, precise_result)
    
    return precise_result
```

---

## 5. Model Selection Strategy

### 5.1 Complexity-to-Model Mapping

```python
MODEL_TIERS = {
    "budget": {
        "complexity_range": (1, 3),
        "models": {
            "cost_first": "Intermediate Model-chat",
            "quality_first": "Basic Model-turbo",
            "balanced": "claude-3-Basic Model"
        },
        "relative_cost": 0.05
    },
    "standard": {
        "complexity_range": (4, 5),
        "models": {
            "cost_first": "Basic Model-turbo",
            "quality_first": "Advanced Model-turbo",
            "balanced": "claude-3-sonnet"
        },
        "relative_cost": 0.15
    },
    "advanced": {
        "complexity_range": (6, 7),
        "models": {
            "cost_first": "claude-3-sonnet",
            "quality_first": "Advanced Model-turbo",
            "balanced": "claude-3-5-sonnet"
        },
        "relative_cost": 0.50
    },
    "expert": {
        "complexity_range": (8, 10),
        "models": {
            "cost_first": "Advanced Model-turbo",
            "quality_first": "claude-3-Advanced Model",
            "balanced": "Advanced Model-turbo"
        },
        "relative_cost": 1.0
    }
}
```

### 5.2 Multi-Factor Model Selection

```python
def select_model(
    complexity: float,
    budget_status: str,  # "sufficient" | "tight" | "critical"
    user_tier: str,      # "free" | "pro" | "enterprise"
    latency_requirement: str,  # "normal" | "fast" | "realtime"
    task_type: Optional[str] = None
) -> ModelSelection:
    
    # Determine tier from complexity
    tier = get_tier_from_complexity(complexity)
    
    # Select strategy based on constraints
    if budget_status == "critical":
        strategy = "cost_first"
    elif user_tier == "enterprise":
        strategy = "quality_first"
    else:
        strategy = "balanced"
    
    # Get base model
    model = MODEL_TIERS[tier]["models"][strategy]
    
    # Apply latency override
    if latency_requirement == "realtime":
        model = apply_latency_preference(model)
    
    # Apply task-specific override
    if task_type:
        model = apply_task_override(model, task_type)
    
    return ModelSelection(
        model=model,
        tier=tier,
        strategy=strategy,
        estimated_cost=estimate_cost(model, complexity)
    )
```

### 5.3 Task-Specific Overrides

```yaml
task_overrides:
  code_generation:
    preferred: "claude-3-5-sonnet"
    reason: "Best code quality"
    
  long_context:
    preferred: "claude-3-5-sonnet"
    reason: "200K context window"
    
  fast_response:
    preferred: "groq/llama-3.1-70b"
    reason: "Lowest latency"
    
  chinese_tasks:
    preferred: "Intermediate Model-chat"
    reason: "Best Chinese performance"
    
  math_reasoning:
    preferred: "Advanced Model-turbo"
    reason: "Best mathematical accuracy"
```

---

## 6. Self-Learning Feedback Loop

### 6.1 Feedback Collection

CostLLM continuously learns from multiple feedback signals:

```python
class FeedbackCollector:
    """
    Collect quality signals from multiple sources.
    """
    
    def collect_feedback(self, request_id: str) -> FeedbackSignals:
        return FeedbackSignals(
            # Explicit feedback
            user_rating=self._get_user_rating(request_id),      # 1-5 stars
            user_regenerated=self._check_regeneration(request_id),  # bool
            
            # Implicit feedback
            response_accepted=self._check_acceptance(request_id),   # bool
            time_to_next_action=self._get_dwell_time(request_id),   # seconds
            
            # Quality metrics
            retry_count=self._get_retry_count(request_id),
            error_occurred=self._check_errors(request_id),
            
            # Cost metrics
            actual_cost=self._get_actual_cost(request_id),
            estimated_cost=self._get_estimated_cost(request_id)
        )
```

### 6.2 Quality Score Calculation

```python
def calculate_quality_score(feedback: FeedbackSignals) -> float:
    """
    Combine feedback signals into a single quality score (0-1).
    """
    score = 0.5  # Base score
    
    # User rating (weight: 0.35)
    if feedback.user_rating:
        score += (feedback.user_rating - 3) * 0.07  # -0.14 to +0.14
    
    # Regeneration penalty (weight: 0.20)
    if feedback.user_regenerated:
        score -= 0.20
    
    # Acceptance bonus (weight: 0.15)
    if feedback.response_accepted:
        score += 0.15
    
    # Retry penalty (weight: 0.15)
    score -= min(feedback.retry_count * 0.05, 0.15)
    
    # Error penalty (weight: 0.15)
    if feedback.error_occurred:
        score -= 0.15
    
    return max(0.0, min(1.0, score))
```

### 6.3 Model Performance Tracking

```python
class ModelPerformanceTracker:
    """
    Track per-model performance across complexity levels.
    """
    
    def update(self, 
               model: str, 
               complexity: float, 
               quality_score: float,
               cost: float,
               latency: float):
        
        complexity_bucket = self._get_bucket(complexity)
        
        self.db.execute("""
            INSERT INTO model_performance 
            (model, complexity_bucket, quality_score, cost, latency, timestamp)
            VALUES (?, ?, ?, ?, ?, NOW())
        """, (model, complexity_bucket, quality_score, cost, latency))
    
    def get_model_stats(self, model: str, complexity_bucket: int) -> ModelStats:
        return self.db.query("""
            SELECT 
                AVG(quality_score) as avg_quality,
                AVG(cost) as avg_cost,
                AVG(latency) as avg_latency,
                COUNT(*) as sample_count
            FROM model_performance
            WHERE model = ? 
              AND complexity_bucket = ?
              AND timestamp > NOW() - INTERVAL '7 days'
        """, (model, complexity_bucket))
```

### 6.4 Routing Rule Optimization

```python
class RoutingOptimizer:
    """
    Periodically optimize routing rules based on collected data.
    """
    
    def optimize(self):
        """
        Run daily optimization to update routing rules.
        """
        for complexity_bucket in range(1, 11):
            # Get performance data for all models at this complexity
            model_stats = {}
            for model in AVAILABLE_MODELS:
                stats = self.tracker.get_model_stats(model, complexity_bucket)
                if stats.sample_count >= MIN_SAMPLES:
                    model_stats[model] = stats
            
            # Calculate cost-effectiveness score
            # Score = quality / (cost * latency_factor)
            scores = {}
            for model, stats in model_stats.items():
                latency_factor = 1 + (stats.avg_latency / 1000)  # Penalize slow models
                scores[model] = stats.avg_quality / (stats.avg_cost * latency_factor)
            
            # Update routing rules
            if scores:
                best_model = max(scores, key=scores.get)
                self._update_routing_rule(complexity_bucket, best_model)
    
    def _update_routing_rule(self, complexity: int, model: str):
        # Only update if significantly better (>10% improvement)
        current = self.get_current_rule(complexity)
        if self._is_significant_improvement(current, model):
            self.db.execute("""
                UPDATE routing_rules 
                SET recommended_model = ?, updated_at = NOW()
                WHERE complexity_bucket = ?
            """, (model, complexity))
```

### 6.5 A/B Testing Framework

```python
class ABTestingRouter:
    """
    Route a percentage of traffic to experimental models.
    """
    
    def __init__(self, experiment_config: dict):
        self.experiment_id = experiment_config["id"]
        self.traffic_split = experiment_config["traffic_split"]
        self.metrics = experiment_config["metrics"]
    
    def route(self, request: Request, baseline_model: str) -> str:
        # Check if request should be in experiment
        if not self._should_experiment(request):
            return baseline_model
        
        # Randomly assign to variant
        rand = random.random()
        cumulative = 0
        
        for variant in self.traffic_split:
            cumulative += variant["weight"] / 100
            if rand < cumulative:
                self._record_assignment(request.id, variant["model"])
                return variant["model"]
        
        return baseline_model
    
    def analyze_results(self) -> ABTestResults:
        """
        Analyze experiment results after sufficient data.
        """
        variants = self.db.query("""
            SELECT 
                model,
                AVG(quality_score) as avg_quality,
                AVG(cost) as avg_cost,
                AVG(latency) as avg_latency,
                COUNT(*) as n
            FROM ab_test_results
            WHERE experiment_id = ?
            GROUP BY model
        """, (self.experiment_id,))
        
        return self._calculate_significance(variants)
```

---

## 7. Cost-Aware Circuit Breaker

### 7.1 Multi-Level Cost Protection

```python
class CostCircuitBreaker:
    """
    Prevent budget overruns with multi-level protection.
    """
    
    THRESHOLDS = {
        "per_request": {
            "warning": 0.50,    # $0.50 per request
            "critical": 1.00,   # $1.00 per request
            "action": "downgrade_model"
        },
        "per_minute": {
            "warning": 5.00,    # $5/minute
            "critical": 10.00,  # $10/minute
            "action": "rate_limit"
        },
        "per_user_daily": {
            "warning": 20.00,   # $20/user/day
            "critical": 50.00,  # $50/user/day
            "action": "user_quota"
        },
        "total_daily": {
            "warning": 500.00,  # $500/day
            "critical": 800.00, # $800/day
            "action": "emergency_mode"
        }
    }
    
    def check_before_request(self, request: Request) -> CircuitStatus:
        estimated_cost = self.estimate_cost(request)
        
        # Check per-request limit
        if estimated_cost > self.THRESHOLDS["per_request"]["critical"]:
            return CircuitStatus.REJECT
        
        # Check rate limits
        current_minute_cost = self.get_minute_cost()
        if current_minute_cost > self.THRESHOLDS["per_minute"]["critical"]:
            return CircuitStatus.RATE_LIMITED
        
        # Check user quota
        user_daily_cost = self.get_user_daily_cost(request.user_id)
        if user_daily_cost > self.THRESHOLDS["per_user_daily"]["critical"]:
            return CircuitStatus.USER_QUOTA_EXCEEDED
        
        # Check total daily
        total_daily = self.get_total_daily_cost()
        if total_daily > self.THRESHOLDS["total_daily"]["critical"]:
            return CircuitStatus.EMERGENCY_MODE
        
        return CircuitStatus.OK
```

### 7.2 Graceful Degradation

```python
class GracefulDegrader:
    """
    Gracefully degrade service when approaching limits.
    """
    
    def apply_degradation(self, 
                          request: Request, 
                          status: CircuitStatus) -> DegradedRequest:
        
        if status == CircuitStatus.OK:
            return request  # No degradation
        
        if status == CircuitStatus.WARNING:
            # Soft degradation: prefer cheaper models
            return self._prefer_cheaper_model(request)
        
        if status == CircuitStatus.RATE_LIMITED:
            # Queue the request
            return self._queue_request(request)
        
        if status == CircuitStatus.USER_QUOTA_EXCEEDED:
            # Notify user, offer upgrade
            return self._notify_quota_exceeded(request)
        
        if status == CircuitStatus.EMERGENCY_MODE:
            # Use only cheapest models
            return self._emergency_routing(request)
    
    def _emergency_routing(self, request: Request) -> DegradedRequest:
        """
        Emergency mode: only use cheapest available model.
        """
        return DegradedRequest(
            original=request,
            model_override="Intermediate Model-chat",
            max_tokens_override=500,
            message="Service in cost-saving mode. Response may be limited."
        )
```

### 7.3 Real-Time Cost Dashboard

```yaml
cost_monitoring:
  real_time_metrics:
    - metric: "cost_per_second"
      aggregation: "sum"
      window: "1s"
      
    - metric: "cost_per_model"
      aggregation: "sum"
      group_by: "model"
      window: "1m"
      
    - metric: "cost_per_user"
      aggregation: "sum"
      group_by: "user_id"
      window: "1h"
  
  alerts:
    - name: "Cost Spike"
      condition: "cost_per_minute > 2 * avg_cost_per_minute_7d"
      action: "notify_ops"
      
    - name: "Budget 80%"
      condition: "daily_cost > daily_budget * 0.8"
      action: "enable_cost_saving_mode"
      
    - name: "Budget Critical"
      condition: "daily_cost > daily_budget * 0.95"
      action: "emergency_mode"
```

---

## 8. Cache Integration

### 8.1 Semantic Cache Layer

```python
class SemanticCache:
    """
    Cache similar requests to avoid redundant LLM calls.
    """
    
    def __init__(self, similarity_threshold: float = 0.95):
        self.threshold = similarity_threshold
        self.embedding_model = "text-embedding-3-small"
    
    def check(self, request: Request) -> Optional[CachedResponse]:
        # Generate embedding for request
        embedding = self._embed(request.messages)
        
        # Search for similar cached requests
        similar = self.vector_store.search(
            embedding,
            threshold=self.threshold,
            limit=1
        )
        
        if similar:
            return CachedResponse(
                content=similar[0].response,
                cache_hit=True,
                similarity=similar[0].score
            )
        
        return None
    
    def store(self, request: Request, response: str):
        embedding = self._embed(request.messages)
        self.vector_store.insert(
            embedding=embedding,
            response=response,
            metadata={
                "model": request.model,
                "complexity": request.complexity,
                "timestamp": datetime.now()
            }
        )
```

### 8.2 Cache-Aware Routing

```python
def route_with_cache(request: Request) -> RoutingResult:
    # Step 1: Check cache first
    cached = semantic_cache.check(request)
    if cached:
        return RoutingResult(
            source="cache",
            response=cached.content,
            cost=0.0
        )
    
    # Step 2: Evaluate complexity
    eval_result = evaluate_complexity(request)
    
    # Step 3: Select model
    model = select_model(
        complexity=eval_result.complexity_score,
        budget_status=get_budget_status(),
        user_tier=request.user.tier
    )
    
    # Step 4: Call LLM
    response = llm_call(model, request)
    
    # Step 5: Cache response
    semantic_cache.store(request, response)
    
    return RoutingResult(
        source="llm",
        model=model,
        response=response,
        cost=calculate_cost(model, request, response)
    )
```

---

## 9. Experimental Evaluation

### 9.1 Experimental Setup

**Dataset**: 10,000 real requests from WizAxis production logs over 30 days, manually labeled with:
- Ground truth complexity (1-10)
- Optimal model selection
- Quality scores from user feedback

**Baselines**:
- **Always-Best**: Always use Advanced Model Turbo
- **Always-Cheap**: Always use Intermediate Model
- **Random**: Random model selection
- **Static-Rules**: Fixed task-type to model mapping
- **FrugalGPT**: Cascading approach (Chen et al., 2023)

**Metrics**:
- Cost per request (USD)
- Quality score (0-1, from user feedback)
- Latency (ms)
- Complexity prediction accuracy

### 9.2 Main Results

| Method | Avg Cost | Quality | Latency | Cost Savings |
|--------|----------|---------|---------|--------------|
| Always-Best | $0.0312 | 0.94 | 2,450ms | 0% (baseline) |
| Always-Cheap | $0.0021 | 0.71 | 890ms | 93% |
| Random | $0.0156 | 0.82 | 1,670ms | 50% |
| Static-Rules | $0.0134 | 0.86 | 1,520ms | 57% |
| FrugalGPT | $0.0098 | 0.89 | 3,200ms | 69% |
| **CostLLM** | **$0.0103** | **0.90** | **1,340ms** | **67%** |

**Key findings**:
1. CostLLM achieves **67% cost reduction** vs Always-Best
2. Quality parity: 0.90 vs 0.94 (96% of best model quality)
3. **Lower latency than FrugalGPT** (no cascading overhead)
4. Outperforms Static-Rules by 10% cost savings with better quality

### 9.3 Complexity Prediction Accuracy

| Eval Method | Accuracy | Precision | Recall | F1 |
|-------------|----------|-----------|--------|-----|
| Fast Eval (all) | 78.3% | 0.76 | 0.79 | 0.77 |
| Fast Eval (conf≥70%) | 89.2% | 0.88 | 0.90 | 0.89 |
| Precise Eval | 91.5% | 0.90 | 0.92 | 0.91 |
| Combined (CostLLM) | 88.7% | 0.87 | 0.89 | 0.88 |

**Insight**: Fast Eval with confidence filtering achieves 89% accuracy at zero cost. Precise Eval adds only 2.3% accuracy improvement at $0.001/call.

### 9.4 Cost Breakdown Analysis

```
Request Distribution by Complexity:
┌─────────────────────────────────────────────────────────┐
│ Complexity 1-3 (Simple):     42% of requests           │
│ Complexity 4-5 (Medium):     31% of requests           │
│ Complexity 6-7 (Complex):    19% of requests           │
│ Complexity 8-10 (Expert):     8% of requests           │
└─────────────────────────────────────────────────────────┘

Cost Savings by Complexity:
┌─────────────────────────────────────────────────────────┐
│ Simple tasks:   95% savings (Intermediate Model vs Advanced Model)        │
│ Medium tasks:   70% savings (Basic Model vs Advanced Model)         │
│ Complex tasks:  40% savings (Claude-3-Sonnet vs Advanced Model) │
│ Expert tasks:    0% savings (Advanced Model required)           │
└─────────────────────────────────────────────────────────┘
```

**Key insight**: 42% of requests are simple tasks where 95% cost savings are possible. This drives the overall 67% cost reduction.

### 9.5 Self-Learning Improvement

| Week | Routing Accuracy | Cost Savings | Quality |
|------|------------------|--------------|---------|
| 1 | 82.1% | 58% | 0.87 |
| 2 | 85.4% | 62% | 0.88 |
| 3 | 87.2% | 65% | 0.89 |
| 4 | 88.7% | 67% | 0.90 |

**Observation**: Self-learning loop improves routing accuracy by 6.6% over 4 weeks, translating to 9% additional cost savings.

### 9.6 Ablation Study

| Configuration | Cost | Quality | Notes |
|---------------|------|---------|-------|
| Full CostLLM | $0.0103 | 0.90 | Complete system |
| - Fast Eval | $0.0118 | 0.90 | +15% cost (all Precise Eval) |
| - Precise Eval | $0.0098 | 0.86 | -4% quality (Fast only) |
| - Self-Learning | $0.0112 | 0.88 | +9% cost, -2% quality |
| - Cache | $0.0128 | 0.90 | +24% cost |
| - Circuit Breaker | $0.0103 | 0.90 | No change (safety feature) |

**Findings**:
- Cache provides 24% cost reduction
- Self-learning contributes 9% cost savings
- Fast Eval saves 15% vs always using Precise Eval

---

## 10. Case Studies

### 10.1 Case Study: E-commerce Customer Service

**Scenario**: 50,000 daily customer queries ranging from "What's my order status?" to "Help me choose between these 5 products"

**Before CostLLM**:
- All queries routed to Advanced Model
- Daily cost: $1,560
- Average latency: 2.8s

**After CostLLM**:
- Simple queries (60%): Intermediate Model
- Medium queries (30%): Basic Model
- Complex queries (10%): Advanced Model
- Daily cost: $312 (80% reduction)
- Average latency: 1.2s (57% faster)
- Quality maintained: 0.92 vs 0.94

### 10.2 Case Study: Code Assistant

**Scenario**: Developer tool with code generation, review, and debugging tasks

**Routing decisions**:
```
"Add a comment to line 5"     → Intermediate Model (complexity: 2)
"Explain this function"       → Basic Model (complexity: 4)
"Refactor for performance"    → Claude-3.5-Sonnet (complexity: 7)
"Design microservices arch"   → Advanced Model (complexity: 9)
```

**Results**:
- 65% cost reduction
- Code quality maintained (measured by test pass rate)
- Developer satisfaction: 4.6/5.0

---

## 11. Discussion

### 11.1 Limitations

1. **Cold Start**: New deployments lack historical data for accurate routing
2. **Domain Shift**: Model performance varies across domains
3. **Rapid Model Updates**: New model releases require re-calibration
4. **Subjective Quality**: User feedback can be noisy

### 11.2 Future Work

1. **Multi-Modal Routing**: Extend to image/audio models
2. **Federated Learning**: Share routing knowledge across deployments
3. **Real-Time Model Benchmarking**: Continuous model capability assessment
4. **Cost Prediction**: Predict output tokens before generation

### 11.3 Ethical Considerations

- **Transparency**: Users should know which model serves their request
- **Fairness**: Avoid routing based on user demographics
- **Quality Guarantees**: Minimum quality thresholds for all users

---

## 12. Conclusion

We presented **CostLLM**, an intelligent routing framework that automatically selects the optimal LLM for each task based on complexity assessment. Our dual-layer evaluation architecture achieves 88.7% routing accuracy while adding minimal latency (<5ms for 85% of requests). The self-learning feedback loop continuously improves routing decisions, achieving 67% cost reduction while maintaining 96% quality parity with always-using-best-model baseline.

**Key takeaways**:
1. **Task complexity varies dramatically** - 42% of requests are simple enough for cheap models
2. **Zero-cost evaluation is possible** - Rule-based Fast Eval handles 85% of routing decisions
3. **Continuous learning matters** - Self-learning improves cost savings by 9% over 4 weeks
4. **Cost protection is essential** - Circuit breakers prevent budget overruns

CostLLM is deployed in production on WizAxis, serving 1,200+ daily users with $15,000+ monthly cost savings.

---

## References

1. Chen, L., et al. (2023). FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance. arXiv:2305.05176.

2. OpenAI. (2024). Advanced Model Technical Report. arXiv:2303.08774.

3. Anthropic. (2024). Advanced Model Model Card.

4. LiteLLM. (2024). Unified Interface for LLM APIs. https://github.com/BerriAI/litellm

5. Jiang, A., et al. (2024). Intermediate Model of Experts. arXiv:2401.04088.

6. Intermediate Model. (2024). Intermediate Model-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model. arXiv:2405.04434.

7. Sheng, Y., et al. (2023). FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU. ICML 2023.

8. Kwon, W., et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention. SOSP 2023.

---

## Appendix A: Model Pricing Reference (January 2026)

| Model | Input ($/1K) | Output ($/1K) | Context | Latency |
|-------|--------------|---------------|---------|---------|
| Advanced Model Turbo | 0.01 | 0.03 | 128K | ~2.5s |
| Basic Model Turbo | 0.0005 | 0.0015 | 16K | ~0.8s |
| Claude-3 Advanced Model | 0.015 | 0.075 | 200K | ~3.0s |
| Claude-3.5 Sonnet | 0.003 | 0.015 | 200K | ~1.5s |
| Claude-3 Basic Model | 0.00025 | 0.00125 | 200K | ~0.5s |
| Intermediate Model Chat | 0.0001 | 0.0002 | 64K | ~0.9s |
| Groq Llama-3.1-70B | 0.0006 | 0.0008 | 128K | ~0.3s |

---

## Appendix B: Fast Eval Keyword Dictionary

```yaml
simple_keywords:
  en: ["what is", "define", "translate", "list", "summarize", "convert"]
  zh: ["是什么", "翻译", "列出", "总结", "转换"]
  
medium_keywords:
  en: ["explain", "compare", "analyze", "why", "how does"]
  zh: ["解释", "比较", "分析", "为什么", "怎么"]
  
complex_keywords:
  en: ["design", "implement", "optimize", "debug", "refactor", "architect"]
  zh: ["设计", "实现", "优化", "调试", "重构", "架构"]
  
expert_keywords:
  en: ["prove", "derive", "distributed", "consensus", "formal verification"]
  zh: ["证明", "推导", "分布式", "共识", "形式化验证"]
```

---

*Corresponding author: [email]*  
*Code and data: https://github.com/[repo]*  
*DOI: 10.5281/zenodo.18207648*
