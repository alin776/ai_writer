"""
Week 7: CostTracker Unit Tests

Test the cost tracking system
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from app.services.agent.cost_tracker import (
    CostTracker,
    APICallRecord,
    CostStatistics,
    get_cost_tracker
)


class TestCostTracker:
    """Test CostTracker class"""

    @pytest.fixture
    def tracker(self):
        """Create a fresh tracker for each test"""
        return CostTracker(enable_persistence=False)

    @pytest.mark.asyncio
    async def test_init(self, tracker):
        """Test initialization"""
        assert tracker.enable_persistence is False
        assert len(tracker._records) == 0

    @pytest.mark.asyncio
    async def test_track_api_call_basic(self, tracker):
        """Test basic API call tracking"""
        record = await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150
        )

        assert isinstance(record, APICallRecord)
        assert record.user_id == "user_001"
        assert record.model_id == "gemini-2.5-flash"
        assert record.input_tokens == 1000
        assert record.output_tokens == 500
        assert record.total_tokens == 1500
        assert record.total_cost == 0.000225
        assert record.success is True

    @pytest.mark.asyncio
    async def test_track_api_call_with_task_info(self, tracker):
        """Test tracking with task information"""
        record = await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-pro",
            model_name="Gemini 2.5 Pro",
            input_tokens=3000,
            output_tokens=2000,
            input_cost=0.00375,
            output_cost=0.01000,
            task_type="content_creation",
            task_complexity="complex",
            work_id="work_123",
            chapter_id="chapter_001"
        )

        assert record.task_type == "content_creation"
        assert record.task_complexity == "complex"
        assert record.work_id == "work_123"
        assert record.chapter_id == "chapter_001"

    @pytest.mark.asyncio
    async def test_track_multiple_calls(self, tracker):
        """Test tracking multiple API calls"""
        # Track 3 calls
        for i in range(3):
            await tracker.track_api_call(
                user_id="user_001",
                model_provider="gemini",
                model_id="gemini-2.5-flash-lite",
                model_name="Gemini 2.5 Flash Lite",
                input_tokens=500 + i * 100,
                output_tokens=300 + i * 50,
                input_cost=0.000015,
                output_cost=0.000036
            )

        assert len(tracker._records) == 3

    @pytest.mark.asyncio
    async def test_get_cost_statistics_all(self, tracker):
        """Test getting overall cost statistics"""
        # Add some records
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150
        )

        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash-lite",
            model_name="Gemini 2.5 Flash Lite",
            input_tokens=500,
            output_tokens=300,
            input_cost=0.000015,
            output_cost=0.000036
        )

        stats = await tracker.get_cost_statistics(
            user_id="user_001",
            period="all"
        )

        assert isinstance(stats, CostStatistics)
        assert stats.total_calls == 2
        assert stats.total_tokens == 2300
        assert abs(stats.total_cost - 0.000276) < 0.000001
        assert stats.avg_tokens_per_call == 1150

    @pytest.mark.asyncio
    async def test_get_cost_statistics_by_model(self, tracker):
        """Test cost statistics breakdown by model"""
        # Add records for different models
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150
        )

        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-pro",
            model_name="Gemini 2.5 Pro",
            input_tokens=2000,
            output_tokens=1000,
            input_cost=0.002500,
            output_cost=0.005000
        )

        stats = await tracker.get_cost_statistics(user_id="user_001")

        assert len(stats.cost_by_model) == 2
        assert "gemini-2.5-flash" in stats.cost_by_model
        assert "gemini-2.5-pro" in stats.cost_by_model
        assert stats.calls_by_model["gemini-2.5-flash"] == 1
        assert stats.calls_by_model["gemini-2.5-pro"] == 1

    @pytest.mark.asyncio
    async def test_get_cost_statistics_by_task_type(self, tracker):
        """Test cost statistics breakdown by task type"""
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150,
            task_type="text_polish"
        )

        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-pro",
            model_name="Gemini 2.5 Pro",
            input_tokens=2000,
            output_tokens=1000,
            input_cost=0.002500,
            output_cost=0.005000,
            task_type="content_creation"
        )

        stats = await tracker.get_cost_statistics(user_id="user_001")

        assert len(stats.cost_by_task_type) == 2
        assert "text_polish" in stats.cost_by_task_type
        assert "content_creation" in stats.cost_by_task_type

    @pytest.mark.asyncio
    async def test_check_cost_limit_within(self, tracker):
        """Test cost limit check - within limit"""
        # Add a small cost record
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash-lite",
            model_name="Gemini 2.5 Flash Lite",
            input_tokens=500,
            output_tokens=300,
            input_cost=0.000015,
            output_cost=0.000036
        )

        result = await tracker.check_cost_limit(
            user_id="user_001",
            period="daily",
            limit=1.0  # $1 limit
        )

        assert result["within_limit"] is True
        assert result["current_cost"] < result["limit"]
        assert result["remaining"] > 0
        assert result["usage_percentage"] < 1

    @pytest.mark.asyncio
    async def test_check_cost_limit_exceeded(self, tracker):
        """Test cost limit check - exceeded"""
        # Add a high cost record
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-pro",
            model_name="Gemini 2.5 Pro",
            input_tokens=100000,
            output_tokens=50000,
            input_cost=0.125,
            output_cost=0.250
        )

        result = await tracker.check_cost_limit(
            user_id="user_001",
            period="daily",
            limit=0.1  # Very low limit
        )

        assert result["within_limit"] is False
        assert result["current_cost"] > result["limit"]
        assert result["remaining"] < 0
        assert result["usage_percentage"] > 100

    @pytest.mark.asyncio
    async def test_get_cost_report(self, tracker):
        """Test cost report generation"""
        # Add some records
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150,
            task_type="text_polish"
        )

        report = await tracker.get_cost_report(
            user_id="user_001",
            period="all"
        )

        assert "summary" in report
        assert "breakdown" in report
        assert report["summary"]["total_calls"] == 1
        assert report["summary"]["total_cost"] == 0.0002
        assert "by_model" in report["breakdown"]
        assert "by_task_type" in report["breakdown"]

    @pytest.mark.asyncio
    async def test_get_recent_records(self, tracker):
        """Test getting recent records"""
        # Add 5 records
        for i in range(5):
            await tracker.track_api_call(
                user_id=f"user_{i:03d}",
                model_provider="gemini",
                model_id="gemini-2.5-flash",
                model_name="Gemini 2.5 Flash",
                input_tokens=1000,
                output_tokens=500,
                input_cost=0.000075,
                output_cost=0.000150
            )

        recent = tracker.get_recent_records(limit=3)

        assert len(recent) == 3
        # Should be in reverse chronological order
        assert recent[0].timestamp >= recent[1].timestamp
        assert recent[1].timestamp >= recent[2].timestamp

    @pytest.mark.asyncio
    async def test_success_rate_calculation(self, tracker):
        """Test success rate calculation"""
        # Add 3 successful calls
        for _ in range(3):
            await tracker.track_api_call(
                user_id="user_001",
                model_provider="gemini",
                model_id="gemini-2.5-flash",
                model_name="Gemini 2.5 Flash",
                input_tokens=1000,
                output_tokens=500,
                input_cost=0.000075,
                output_cost=0.000150,
                success=True
            )

        # Add 1 failed call
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150,
            success=False,
            error_message="API Error"
        )

        stats = await tracker.get_cost_statistics(user_id="user_001")

        assert stats.success_rate == 0.75  # 3/4 = 75%

    @pytest.mark.asyncio
    async def test_multi_user_tracking(self, tracker):
        """Test tracking for multiple users"""
        # User 1
        await tracker.track_api_call(
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            input_cost=0.000075,
            output_cost=0.000150
        )

        # User 2
        await tracker.track_api_call(
            user_id="user_002",
            model_provider="gemini",
            model_id="gemini-2.5-pro",
            model_name="Gemini 2.5 Pro",
            input_tokens=2000,
            output_tokens=1000,
            input_cost=0.002500,
            output_cost=0.005000
        )

        stats1 = await tracker.get_cost_statistics(user_id="user_001")
        stats2 = await tracker.get_cost_statistics(user_id="user_002")

        assert stats1.total_calls == 1
        assert stats2.total_calls == 1
        assert stats1.total_cost < stats2.total_cost


class TestGlobalCostTracker:
    """Test global cost tracker singleton"""

    def test_get_cost_tracker_singleton(self):
        """Test that get_cost_tracker returns singleton"""
        tracker1 = get_cost_tracker()
        tracker2 = get_cost_tracker()

        assert tracker1 is tracker2  # Same instance


class TestAPICallRecord:
    """Test APICallRecord model"""

    def test_create_record(self):
        """Test creating a record"""
        record = APICallRecord(
            id="test_001",
            user_id="user_001",
            model_provider="gemini",
            model_id="gemini-2.5-flash",
            model_name="Gemini 2.5 Flash",
            input_tokens=1000,
            output_tokens=500,
            total_tokens=1500,
            input_cost=0.000075,
            output_cost=0.000150,
            total_cost=0.000225
        )

        assert record.id == "test_001"
        assert record.total_tokens == 1500
        assert record.total_cost == 0.000225
        assert record.success is True


class TestCostStatistics:
    """Test CostStatistics model"""

    def test_create_statistics(self):
        """Test creating statistics"""
        stats = CostStatistics(
            period="daily",
            start_date=datetime.now(),
            end_date=datetime.now(),
            total_calls=10,
            total_tokens=15000,
            total_cost=0.05
        )

        assert stats.period == "daily"
        assert stats.total_calls == 10
        assert stats.total_tokens == 15000
        assert stats.total_cost == 0.05


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
