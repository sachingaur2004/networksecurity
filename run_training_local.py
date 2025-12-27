from networksecurity.pipeline.training_pipeline import TrainingPipeline

print("🚀 Starting standalone training...")

tp = TrainingPipeline()
tp.run_pipeline()

print("✅ Training finished (check local folders + S3)")
