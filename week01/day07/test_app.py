from fastapi.testclient import TestClient

from app import app

from unittest.mock import patch


client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    #response = client.get("/api/v1/analyses")
    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }

def test_analyze():
    #假定结果
    fake_result = {
        "success": True,
        "model": "test-model",
        "content": "测试分析结果",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
    }
    #patch,替换掉analyzer里的analyze_with_model,return结果换成fake_result
    with patch(
        "analyzer.analyze_with_model",
        return_value = fake_result,
    ),patch(
         "analyzer.save_analysis"
    ) as mock_save:
        response = client.post(
            "/api/v1/analyze",
            json={
                "report_file": "report.json"
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "分析成功"
    assert data["data"]["model"] == "test-model"
    assert data["data"]["content"] == "测试分析结果"
    mock_save.assert_called_once()
def test_analyze_invalid_file():
    response = client.post(
        "/api/v1/analyze",
        json={
            "report_file": "../test.txt"
        },
    )

    assert response.status_code == 422


def test_analyze_not_exist_file():
    response = client.post(
        "/api/v1/analyze",
        json={
            "report_file": "test.json"
        },
    )

    assert response.status_code == 404
    data = response.json()

    assert data["success"] is False
    assert "不存在" in data["message"]
    assert data["data"] is None

def test_analyze_model_failed():
    #需要访问模型的给了个虚拟的返回，不需要访问模型的报错直接按照exceptions里面的返回操作
    fake_result={
        "success":False,
        "error":"模型调用失败",
    }
    with patch(
        "analyzer.analyze_with_model",
        return_value = fake_result,
    ),patch(
         "analyzer.save_analysis"
    ) as mock_save:
        response = client.post(
            "/api/v1/analyze",
            json={
                "report_file": "report.json"
            },
        )

    assert response.status_code == 502
    data = response.json()
    assert data["success"] is False
    assert data["message"] =="模型调用失败"
    assert data["data"] is None
    mock_save.assert_not_called()
def test_get_analyses():
    fake_records = [
        {
            "id": 1,
            "report_file": "report.json",
            "model": "test-model",
            "content": "测试分析结果",
            "created_at": "2026-08-17 10:00:00",
        }
    ]

    with patch(
        "routes.get_analysis_records",
        return_value = fake_records,
    ):
        response = client.get(
            "/api/v1/analyses?limit=20"
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "查询成功"
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1
    assert data["data"][0]["model"] == "test-model"
    assert data["data"][0]["report_file"] == "report.json"

def test_get_analyses_by_id():
    fake_record = {
            "id": 1,
            "report_file": "report.json",
            "model": "test-model",
            "content": "测试分析结果",
            "created_at": "2026-08-17 10:00:00",
        }
    with patch(
            "routes.get_analysis_by_id",
            return_value = fake_record,
        ):
            response = client.get(
                "/api/v1/analyses/1"
            )
    assert response.status_code ==200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "查询成功"
    #assert len(data["data"]) == 1
    assert data["data"]["id"] == 1
    assert data["data"]["model"] == "test-model"
    assert data["data"]["report_file"] == "report.json"

def test_get_analyses_by_id_not_found():
    with patch(
        "routes.get_analysis_by_id",
        return_value = None,
    ):
        response = client.get(
             "/api/v1/analyses/1"
        )
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "无对应记录"
        assert data["data"] is None

def test_del_by_id():
        with patch(
            "routes.del_analysis_by_id",
            return_value = True,
        ):
            response = client.delete(
                "/api/v1/analyses/999"
            )
        assert response.status_code==200
        data = response.json()
        assert data["success"] is True
        assert data["message"] =="删除成功"
        assert data["data"] is None

def test_delete_analysis_not_found():
     with patch(
        "routes.del_analysis_by_id",
        return_value=False,
     ):
        response = client.delete(
          "/api/v1/analyses/999"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["message"] =="无对应记录"
        assert data["data"] is None
