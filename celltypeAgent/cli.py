import click
import time
from celltypeAgent.workflow import CelltypeWorkflow
from celltypeAgent.tools.logger import (
    console, log_error, log_success, display_status_panel
)


VERSION = "1.0.0"


@click.group()
def cli():
    """✨ CelltypeAgent - 单细胞 RNA 序列数据细胞类型注释工具"""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', required=True, help='输出目录')
@click.option('-p', '--provider', default='n1n', help='API provider (默认: n1n)')
def annotate(input_file, output, provider):
    """执行完整的细胞类型注释流程
    
    INPUT: 输入文件路径 (CSV 格式的 marker 基因表)
    """
    console.clear()
    
    display_status_panel("运行参数", {
        "输入文件": input_file,
        "输出目录": output,
        "Provider": provider
    })
    
    try:
        console.print()
        console.print("[bold magenta]✨ 初始化工作流...[/bold magenta]")
        
        runner = CelltypeWorkflow(input_file, output, provider)
        time.sleep(10) 
        console.print()
        console.print("[bold magenta]✨ 开始参数收集...[/bold magenta]")
        
        runner.collect_parms()
        
        console.print()
        console.print("[bold magenta]✨ 开始多 Cluster 注释...[/bold magenta]")
        
        runner.multi_cluster_annotation()
        
        console.print()
        log_success("所有任务完成！")
        
    except Exception as e:
        console.print()
        log_error(f"执行失败: {str(e)}")
        raise click.Abort()


@cli.command()
def version():
    """显示版本信息"""
    console.print(f"[bold magenta]✨ CelltypeAgent[/bold magenta] version [cyan]{VERSION}[/cyan]")


def main():
    cli()


if __name__ == '__main__':
    main()
