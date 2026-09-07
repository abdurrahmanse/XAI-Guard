export default function AboutPage() {
  return (
    <div className="flex-1 py-24 max-w-4xl mx-auto px-6 w-full text-center">
      <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-8">About XAI-Guard</h1>
      <p className="text-xl text-muted-foreground leading-relaxed mb-6">
        XAI-Guard was founded on a simple principle: Machine Learning in cybersecurity should not be a black box. 
        Security analysts need to know exactly <strong>why</strong> a model blocked a transaction or flagged an IP.
      </p>
      <p className="text-xl text-muted-foreground leading-relaxed">
        By combining State-of-the-Art ML models (XGBoost, Isolation Forests) with SHAP and LIME algorithms, 
        we provide the world's most transparent threat detection platform.
      </p>
    </div>
  );
}
