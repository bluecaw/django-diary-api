# Django Diary API

Power Appsから利用するDiary APIの学習プロジェクト。

## Architecture

```text
Power Apps
    ↓
Microsoft Entra ID
    ↓
Custom Connector
    ↓
Django REST Framework
    ↓
Diary API
    ↓
Diary Database
    ↓
AI Analysis
```

## Learning Roadmap

### Phase 1
- Django
- Django REST Framework
- Microsoft Entra ID
- OAuth 2.0
- Custom Connector
- Power Apps
- Diary CRUD API

### Phase 2
- Transformers
- PyTorch
- 日本語AIモデル
- CPU推論

### Phase 3
- DjangoからAIを呼び出す
- good / bad / cool判定
- AIコメント生成
- SerializerによるAI結果の検証

### Phase 4
- CPU性能測定
- GPU環境の検討
- AIサーバー分離
- GPUクラウドへの移行

## Important

This project is independent from the existing Report API project.
