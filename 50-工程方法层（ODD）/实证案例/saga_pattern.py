from typing import Callable, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"


@dataclass
class SagaStep:
    name: str
    execute: Callable[..., Any]
    compensate: Callable[..., Any]
    execute_args: tuple = ()
    execute_kwargs: dict = None
    compensate_args: tuple = ()
    compensate_kwargs: dict = None

    def __post_init__(self):
        if self.execute_kwargs is None:
            self.execute_kwargs = {}
        if self.compensate_kwargs is None:
            self.compensate_kwargs = {}


class SagaExecutionContext:
    def __init__(self):
        self.results = {}
        self.executed_steps = []

    def add_result(self, step_name: str, result: Any):
        self.results[step_name] = result

    def get_result(self, step_name: str) -> Any:
        return self.results.get(step_name)

    def add_executed_step(self, step: SagaStep):
        self.executed_steps.append(step)


class Saga:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[SagaStep] = []
        self.status = SagaStatus.PENDING
        self.context = SagaExecutionContext()
        self.error: Optional[Exception] = None

    def add_step(
        self,
        name: str,
        execute: Callable,
        compensate: Callable,
        execute_args: tuple = (),
        execute_kwargs: dict = None,
        compensate_args: tuple = (),
        compensate_kwargs: dict = None,
    ) -> "Saga":
        step = SagaStep(
            name=name,
            execute=execute,
            compensate=compensate,
            execute_args=execute_args,
            execute_kwargs=execute_kwargs or {},
            compensate_args=compensate_args,
            compensate_kwargs=compensate_kwargs or {},
        )
        self.steps.append(step)
        return self

    def execute(self) -> bool:
        self.status = SagaStatus.RUNNING
        logger.info(f"Starting saga: {self.name}")

        try:
            for step in self.steps:
                logger.info(f"Executing step: {step.name}")
                try:
                    result = step.execute(*step.execute_args, **step.execute_kwargs)
                    self.context.add_result(step.name, result)
                    self.context.add_executed_step(step)
                    logger.info(f"Step {step.name} completed successfully")
                except Exception as e:
                    logger.error(f"Step {step.name} failed: {str(e)}")
                    self.error = e
                    self.status = SagaStatus.FAILED
                    self._compensate()
                    return False

            self.status = SagaStatus.COMPLETED
            logger.info(f"Saga {self.name} completed successfully")
            return True

        except Exception as e:
            logger.error(f"Saga {self.name} failed with unexpected error: {str(e)}")
            self.error = e
            self.status = SagaStatus.FAILED
            self._compensate()
            return False

    def _compensate(self):
        self.status = SagaStatus.COMPENSATING
        logger.info(f"Starting compensation for saga: {self.name}")

        for step in reversed(self.context.executed_steps):
            logger.info(f"Compensating step: {step.name}")
            try:
                step.compensate(*step.compensate_args, **step.compensate_kwargs)
                logger.info(f"Step {step.name} compensated successfully")
            except Exception as e:
                logger.error(f"Compensation failed for step {step.name}: {str(e)}")

        self.status = SagaStatus.COMPENSATED
        logger.info(f"Saga {self.name} compensation completed")

    def get_status(self) -> SagaStatus:
        return self.status

    def get_error(self) -> Optional[Exception]:
        return self.error

    def get_result(self, step_name: str) -> Any:
        return self.context.get_result(step_name)


# 使用示例
if __name__ == "__main__":
    # 模拟业务操作
    def create_order(order_id: str):
        print(f"Creating order: {order_id}")
        return {"order_id": order_id, "status": "created"}

    def cancel_order(order_id: str):
        print(f"Cancelling order: {order_id}")

    def reserve_inventory(item_id: str, quantity: int):
        print(f"Reserving {quantity} units of item: {item_id}")
        return {"reserved": True}

    def release_inventory(item_id: str, quantity: int):
        print(f"Releasing {quantity} units of item: {item_id}")

    def process_payment(amount: float):
        print(f"Processing payment: ${amount}")
        # 模拟支付失败
        raise Exception("Payment gateway timeout")

    def refund_payment(amount: float):
        print(f"Refunding payment: ${amount}")

    # 创建并执行Saga
    saga = Saga("OrderProcessingSaga")
    saga.add_step(
        name="CreateOrder",
        execute=create_order,
        compensate=cancel_order,
        execute_args=("ORDER-123",),
        compensate_args=("ORDER-123",),
    )
    saga.add_step(
        name="ReserveInventory",
        execute=reserve_inventory,
        compensate=release_inventory,
        execute_args=("ITEM-456", 2),
        compensate_args=("ITEM-456", 2),
    )
    saga.add_step(
        name="ProcessPayment",
        execute=process_payment,
        compensate=refund_payment,
        execute_args=(99.99,),
        compensate_args=(99.99,),
    )

    success = saga.execute()
    print(f"\nSaga execution result: {'Success' if success else 'Failed'}")
    print(f"Final status: {saga.get_status().value}")
    if saga.get_error():
        print(f"Error: {saga.get_error()}")