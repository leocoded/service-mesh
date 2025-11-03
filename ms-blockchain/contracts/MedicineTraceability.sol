// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MedicineTraceability {
    struct TraceRecord {
        string loteId;
        string productoId;
        string ipfsHash;
        uint256 timestamp;
        address registeredBy;
        TraceEventType eventType;
    }
    
    enum TraceEventType {
        CREATED,
        UPDATED,
        RESERVED,
        MOVED,
        EXPIRED
    }
    
    mapping(bytes32 => TraceRecord) public records;
    mapping(string => bytes32[]) public loteHistory;
    
    event TraceRecorded(
        bytes32 indexed recordId,
        string indexed loteId,
        TraceEventType eventType,
        string ipfsHash
    );
    
    function recordTrace(
        string memory _loteId,
        string memory _productoId,
        string memory _ipfsHash,
        TraceEventType _eventType
    ) public returns (bytes32) {
        bytes32 recordId = keccak256(
            abi.encodePacked(_loteId, _productoId, block.timestamp, msg.sender)
        );
        
        records[recordId] = TraceRecord({
            loteId: _loteId,
            productoId: _productoId,
            ipfsHash: _ipfsHash,
            timestamp: block.timestamp,
            registeredBy: msg.sender,
            eventType: _eventType
        });
        
        loteHistory[_loteId].push(recordId);
        
        emit TraceRecorded(recordId, _loteId, _eventType, _ipfsHash);
        
        return recordId;
    }
    
    function getRecord(bytes32 _recordId) public view returns (TraceRecord memory) {
        return records[_recordId];
    }
    
    function getLoteHistory(string memory _loteId) public view returns (bytes32[] memory) {
        return loteHistory[_loteId];
    }
    
    function verifyRecord(bytes32 _recordId) public view returns (bool) {
        return records[_recordId].timestamp > 0;
    }
}