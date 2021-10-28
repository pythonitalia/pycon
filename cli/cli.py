import time
import sys
import signal

import subprocess
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from dataclasses import dataclass
app = typer.Typer()
from rich.live import Live
from enum import Enum
import json
from rich.progress import Progress


class ServiceStatus(Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    RUNNING = 'running'
    STARTING = 'starting'
    EXITED = 'exited'
    UNKNOWN = 'unknown'
    WAITING = 'waiting'

    def to_message(self):
        if self == self.RUNNING or self == self.HEALTHY:
            return '[bold green]:white_check_mark: Running[/bold green]'

        if self == self.STARTING:
            return '[purple]:airplane_departure: Starting[/purple]'

        if self == self.UNHEALTHY:
            return '[red]:exclamation: Unhealthy[/red]'

        if self == self.EXITED:
            return '[red]:no_entry_sign: Exited[/red]'

        if self == self.WAITING:
            return '[dim cyan]:hourglass: Waiting[/dim cyan]'

@dataclass
class StatusRequest:
    status: ServiceStatus
    failing_streak: int = 0

    def to_message(self) -> str:
        if self.status == ServiceStatus.UNHEALTHY and self.failing_streak > 0:
            return f'{self.status.to_message()} [{self.failing_streak}]'
        elif self.status == ServiceStatus.UNHEALTHY and self.failing_streak == 0:
            return ServiceStatus.WAITING.to_message()

        if self.status == ServiceStatus.HEALTHY:
            return self.status.to_message()

        return self.status.to_message()

@dataclass
class Service:
    container_name: str
    name: str
    has_healthcheck: bool = True

    def port(self) -> Optional[int]:
        result = subprocess.run(
            ['docker', 'inspect', '-f', "'{{range $p, $conf := .NetworkSettings.Ports}}{{(index $conf 0).HostPort}}{{end}}'", self.container_name],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return None

        cleaned = result.stdout.strip().replace("'", "")

        if not cleaned:
            return None

        return int(cleaned)

    def status(self) -> StatusRequest:
        if self.has_healthcheck:
            result = subprocess.run(
                ['docker', 'container', 'inspect', '-f', "'{{json .State.Health}}'", self.container_name],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ['docker', 'container', 'inspect', '-f', "'{{json .State.Status}}'", self.container_name],
                capture_output=True,
                text=True
            )

        if result.returncode != 0:
            return StatusRequest(
                status=ServiceStatus.UNKNOWN,
            )

        output = result.stdout.strip().replace("'", "")
        if output == 'null':
            return StatusRequest(
                status=ServiceStatus.UNKNOWN,
            )

        json_output = json.loads(output)

        if self.has_healthcheck:
            status = ServiceStatus(json_output['Status'])
            failing_streak = json_output['FailingStreak']
        else:
            status = ServiceStatus(json_output)
            failing_streak = 0

        return StatusRequest(
            status=status,
            failing_streak=failing_streak
        )


SERVICES = [
    Service(container_name='pycon_pycon-backend_1', name='PyCon Backend'),
    Service(container_name='pycon_users-backend_1', name='Users Backend'),
    Service(container_name='pycon_association-backend_1', name='Association Backend'),
    Service(container_name='pycon_gateway_1', name='GraphQL Gateway'),
    Service(container_name='pycon_association-frontend_1', name='Association Frontend', has_healthcheck=False),
    Service(container_name='pycon_pycon-frontend_1', name='PyCon Frontend', has_healthcheck=False),
]

def create_services_table():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Service")
    table.add_column("Status")
    table.add_column("URL")
    for service in SERVICES:
        status_request = service.status()
        status_message = status_request.to_message()
        port = service.port()

        table.add_row(
            f'[bold]{service.name}',
            status_message,
            f"http://localhost:{port}" if port else 'Not available yet',
        )
    return table

@app.command()
def dev():
    console = Console()
    console.print(':wave: Starting your local environment via Docker now')

    docker_process = subprocess.Popen(
        ['docker-compose', 'up'],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )

    try:
        with Live(create_services_table(), transient=True, auto_refresh=False) as live:
            while True:
                time.sleep(1)
                live.update(create_services_table(), refresh=True)
    except KeyboardInterrupt:
        with console.status("[bold green] Closing Containers"):
            docker_process.send_signal(signal.SIGINT)
            docker_process.wait()

        console.print(":snake: Done.")
        sys.exit(0)


@app.command()
def version():
    return '1.0'
