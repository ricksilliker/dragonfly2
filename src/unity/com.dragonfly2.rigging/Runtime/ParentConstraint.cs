using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ParentConstraint : MonoBehaviour
{
    [Range(0f, 1f)] public float weight = 1f;
    public Transform target;
    public bool maintainOffset;
        
    private Vector3 restPosition;
    private Quaternion restRotation;

    private Vector3 fwd;
    private Vector3 up;
    void Start()
    {
        restPosition = transform.position;
        restRotation = transform.rotation;
        
        fwd = target.InverseTransformDirection(transform.forward);
        up = target.InverseTransformDirection(transform.up);
    }

    void LateUpdate()
    {
        if (maintainOffset)
        {
            Vector3 newPosition = target.TransformPoint(restPosition);
            transform.position = newPosition;

            Quaternion newRotation = Quaternion.LookRotation(target.TransformDirection(fwd), target.TransformDirection(up));
            transform.rotation = newRotation;            
        }
        else
        {
            transform.position = target.position;
            transform.rotation = target.rotation;
        }

    }
}
