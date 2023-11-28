from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller

def helmChart():
    # Helm 차트 정보
    chart_name = "nginx"
    chart_version = "1.0.0"
    chart_values = {"replicaCount": 2}

    # Helm 차트 빌드
    chart = ChartBuilder(
        {"name": chart_name, "version": chart_version, "source": {"path": "path/to/your/chart/source"}},
        chart_values
    )
    chart.save()

    # Helm 차트 배포
    release_name = "my-nginx"  # 배포할 Helm 차트의 릴리스 이름
    namespace = "default"  # 배포할 Helm 차트가 위치한 네임스페이스

    tiller = Tiller(host="localhost", port=44134)  # Tiller가 실행 중인 호스트와 포트로 설정

    tiller.install_release(
        chart_path=chart.chart_dir,
        release_name=release_name,
        namespace=namespace,
        dry_run=False,  # 실제로 실행할 것인지 여부
        values=chart_values,
    )

    print(f"Helm Chart '{release_name}' 배포 완료.")

if __name__ == "__main__":
    helmChart()