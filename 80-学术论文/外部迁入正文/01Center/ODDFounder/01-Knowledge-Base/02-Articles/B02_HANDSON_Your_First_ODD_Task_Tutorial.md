# B02: Hands-On Tutorial - Your First ODD Task

> **作者**: Yi Fu (ODDFounder  fuyi.it@live.cn)
> **类型**: 实战教程
> **难度**: 入门级
> **预计时间**: 15分钟

---

## 教程目标

完成本教程后，你将：
1. 理解 ODD 的核心思维方式
2. 学会定义一个标准的 ODD 契约
3. 体验从契约到产出物的完整流程

---

## 场景：创建一个转账函数

假设你需要实现一个银行转账功能。传统方式是直接写代码，ODD 方式是先定义契约。

---

## 第一步：Define（定义契约）

### 1.1 确定产出物类型

问自己：我需要什么类型的产出物？

- 数据库函数？→ `pg_function`
- Python 类？→ `python_class`
- API 接口？→ `fastapi_endpoint`

本例选择：`pg_function`（PostgreSQL 存储过程）

### 1.2 定义输入输出

```yaml
contract:
  name: transfer_money
  type: pg_function
  
  input:
    from_account: uuid      # 转出账户
    to_account: uuid        # 转入账户
    amount: decimal(10,2)   # 转账金额
  
  output:
    success: boolean        # 是否成功
    transaction_id: uuid    # 交易ID
    message: text           # 结果消息
```

### 1.3 定义前置条件（Preconditions）

```yaml
  preconditions:
    - from_account EXISTS IN accounts
    - to_account EXISTS IN accounts
    - from_account.balance >= amount
    - amount > 0
```

### 1.4 定义后置条件（Postconditions）

```yaml
  postconditions:
    - from_account.balance = OLD.balance - amount
    - to_account.balance = OLD.balance + amount
    - NEW transaction record created
```

---

## 第二步：Decompose（分解任务）

ODD 会自动将大任务分解为小任务：

```
transfer_money (pg_function)
├── 1. 验证账户存在性
├── 2. 检查余额充足
├── 3. 扣减转出账户
├── 4. 增加转入账户
├── 5. 记录交易日志
└── 6. 返回结果
```

---

## 第三步：Execute（执行生成）

将契约交给 AI，它会生成符合契约的代码：

```sql
CREATE OR REPLACE FUNCTION transfer_money(
    p_from_account UUID,
    p_to_account UUID,
    p_amount DECIMAL(10,2)
) RETURNS TABLE(success BOOLEAN, transaction_id UUID, message TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_from_balance DECIMAL(10,2);
    v_txn_id UUID := gen_random_uuid();
BEGIN
    -- 检查账户存在
    IF NOT EXISTS (SELECT 1 FROM accounts WHERE id = p_from_account) THEN
        RETURN QUERY SELECT FALSE, NULL::UUID, 'Source account not found';
        RETURN;
    END IF;
    
    -- 检查余额
    SELECT balance INTO v_from_balance FROM accounts WHERE id = p_from_account;
    IF v_from_balance < p_amount THEN
        RETURN QUERY SELECT FALSE, NULL::UUID, 'Insufficient balance';
        RETURN;
    END IF;
    
    -- 执行转账
    UPDATE accounts SET balance = balance - p_amount WHERE id = p_from_account;
    UPDATE accounts SET balance = balance + p_amount WHERE id = p_to_account;
    
    -- 记录交易
    INSERT INTO transactions(id, from_acc, to_acc, amount) 
    VALUES (v_txn_id, p_from_account, p_to_account, p_amount);
    
    RETURN QUERY SELECT TRUE, v_txn_id, 'Transfer successful';
END;
$$;
```

---

## 第四步：Verify（验证）

运行测试用例验证契约是否满足：

```sql
-- 测试1：正常转账
SELECT * FROM transfer_money('acc-001', 'acc-002', 100.00);
-- 期望：success=true

-- 测试2：余额不足
SELECT * FROM transfer_money('acc-001', 'acc-002', 999999.00);
-- 期望：success=false, message='Insufficient balance'

-- 测试3：账户不存在
SELECT * FROM transfer_money('invalid-id', 'acc-002', 100.00);
-- 期望：success=false, message='Source account not found'
```

---

## 第五步：Seal（封版）

验证通过后，封版归档：
- 契约文件：`contracts/transfer_money.yaml`
- 代码文件：`sql/functions/transfer_money.sql`
- 测试文件：`tests/test_transfer_money.sql`

---

## 核心要点

1. **先定义，后实现**：不要急着写代码，先想清楚要什么
2. **契约即文档**：契约本身就是最好的需求文档
3. **可验证性**：每个产出物都必须可验证
4. **AI 是执行者**：你是架构师，AI 是工人

---

## 下一步

恭喜完成第一个 ODD 任务！接下来可以尝试：
- 《ODD Cookbook：常用任务模板》
- 《17层上下文工程详解》

---

*这就是 Progee 每天在后台自动做成千上万次的事情。当你掌握了这个思维，你就是一个单人软件工厂。*

---

> **ODD Series | Week 32 . Friday | 40 Weeks Total**
> Previous: "方法论-脚本：B01"
> Next: "为什么用户只需点几个同意"
