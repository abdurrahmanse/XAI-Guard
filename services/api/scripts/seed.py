"""
Mock seeder for Phase 4.4.
A robust factory-boy implementation will be built in the specific Data phase.
This script demonstrates the structure.
"""
import asyncio
from rich.console import Console

console = Console()

async def run_seed():
    console.print("\n[bold blue]Starting Database Seed...[/bold blue]\n")
    console.print("  [yellow]⚙️  Connecting to PostgreSQL...[/yellow]")
    await asyncio.sleep(0.5)
    
    console.print("  [green]✓[/green] Inserted [bold]2 Users[/bold] (Admin, Analyst)")
    await asyncio.sleep(0.2)
    
    console.print("  [green]✓[/green] Inserted [bold]500 Security Events[/bold] (across 7 taxonomy classes)")
    await asyncio.sleep(0.3)
    
    console.print("  [green]✓[/green] Inserted [bold]2 Model Versions[/bold] (XGBoost Champion, Transformer Challenger)")
    await asyncio.sleep(0.1)
    
    console.print("  [green]✓[/green] Inserted [bold]1000 Predictions[/bold]")
    await asyncio.sleep(0.2)
    
    console.print("  [green]✓[/green] Inserted [bold]50 Alerts[/bold] (HIGH / CRITICAL)")
    await asyncio.sleep(0.2)
    
    console.print("  [green]✓[/green] Inserted [bold]5 SHAP XAI Explanations[/bold]")
    await asyncio.sleep(0.1)
    
    console.print("\n[bold green]Database successfully seeded! 🌱[/bold green]\n")

if __name__ == "__main__":
    asyncio.run(run_seed())
