# Why Algorithmic Fairness Cannot Be Fully Achieved: A Structural View

---

## 1. The Surface Conflict

Algorithms aim to make decisions fairly.
Different fairness metrics conflict with each other.
Optimizing for one fairness criterion violates another.
The more "fair" the algorithm, the more complex the trade-offs.

The problem is not poor algorithm design.
The problem is not insufficient data.
The problem is structure.

---

## 2. The Hidden Tensions

Two core tensions define this conflict:

- **Group Fairness** — treating similar groups equally
- **Individual Fairness** — treating similar individuals equally

These definitions can diverge significantly in practice.
A decision that is fair across groups may be unfair to specific individuals, and vice versa.

---

## 3. Structural Mapping (ASTO Framework)

Abstract the problem into:

- **Attribute Set A**: The group classification criteria set
- **Attribute Set B**: The individual feature set

The overlap between A and B is imperfect.
Optimizing A requires ignoring some B variance. Optimizing B requires ignoring some A classification.

This creates:

> A structural impossibility of simultaneously satisfying all fairness criteria at maximum levels.

---

## 4. What If We Change the Constraints?

Hypothetical scenarios:

- **Enforce perfect group fairness** → Individual fairness degrades
- **Enforce perfect individual fairness** → Group statistics diverge, discrimination claims emerge
- **Combine fairness metrics** → Trade-off surfaces, but no metric is maximized

This is structural conservation.
Not a matter of better algorithms.

---

## 5. The ASTO Advantage

> Algorithmic fairness is not a single optimization target.
> It is a multi-dimensional constraint space where improving one dimension necessarily degrades others.

Traditional analysis seeks the "right" fairness metric.
ASTO reveals this is a structural impossibility: fairness is a constraint space, not an optimization target.

The solution is not finding the perfect fairness metric.
The solution is explicitly defining which fairness constraints are prioritized — and accepting the structural trade-offs.
