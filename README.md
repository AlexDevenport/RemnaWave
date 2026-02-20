**Тестовое задание RemnaWave API управления**

МОДЕЛЬ ДАННЫХ (минимум)
Client: id (UUID), status (active/blocked), expiresAt (timestamp), createdAt, updatedAt.
Operations/Audit: id, clientId, action, payload (json), result (success/fail), error (text), createdAt.

API (минимум)
1) Клиенты
POST /clients — создать клиента. Ответ: {id}.
GET /clients — список. Фильтры: status (active/blocked), expired (true/false).
GET /clients/{id} — карточка клиента.
DELETE /clients/{id} — удалить/деактивировать (поведение описать в README).
2) Подписка
POST /clients/{id}/extend — продлить на N дней (body: {days:int}). Обновляет expiresAt.
3) Доступ
POST /clients/{id}/block — заблокировать (доступ должен быть отключен в RemnaWave).
POST /clients/{id}/unblock — разблокировать.
4) Конфигурация
GET /clients/{id}/config — получить данные подключения/конфиг (формат описать).
POST /clients/{id}/config/rotate — перевыпустить конфиг/ключ (если применимо; если нет — объяснить и предложить эквивалентную операцию).

ПЛЮС-ФУНКЦИИ (сделать минимум 1)
Аудит всех операций (таблица operations) + эндпоинт GET /operations?clientId=...
Авто-деактивация просроченных: команда/джоба, которая отключает клиентов с expiresAt < now и пишет аудит.
Идемпотентность/защита от дублей для ключевых операций (create/extend).

ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ
API должно корректно валидировать входные данные и отдавать ошибки в JSON (HTTP codes + message).
Хранилище: PostgreSQL
Docker Compose: сервис + БД одной командой запуска.
Тесты:  1–2 unit теста на бизнес-логику
