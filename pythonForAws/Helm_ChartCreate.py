import os
import yaml

def create_helm_chart(chart_name, chart_version, output_dir):
    # Helm 차트 디렉토리 생성
    chart_dir = os.path.join(output_dir, chart_name)
    os.makedirs(chart_dir)

    # Chart.yaml 파일 생성
    chart_yaml = {
        "apiVersion": "v2",
        "name": chart_name,
        "version": chart_version,
        "description": f"A Helm chart for {chart_name}",
    }
    with open(os.path.join(chart_dir, "Chart.yaml"), "w") as chart_file:
        yaml.dump(chart_yaml, chart_file, default_flow_style=False)

    # values.yaml 파일 생성 (선택 사항)
    values_yaml = {
        "replicaCount": 2,
        "image": {"repository": "nginx", "tag": "stable"},
    }
    with open(os.path.join(chart_dir, "values.yaml"), "w") as values_file:
        yaml.dump(values_yaml, values_file, default_flow_style=False)

    # 특정 리소스 파일이나 템플릿을 생성할 수도 있습니다.
    # 예를 들어, templates 디렉토리 생성 후 nginx-deployment.yaml 파일 생성 등...

    print(f"Helm Chart '{chart_name}'를 '{chart_dir}'에 생성했습니다.")

if __name__ == "__main__":
    create_helm_chart("test-helm", "0.0.1", "./tmpChart")