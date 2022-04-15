using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AimConstraint : MonoBehaviour
{
    public Vector3 aimAxis;
    public Vector3 upAxis;
    public Transform target;
    public Transform upObject;
    public Vector3 worldUpAxis;
    public bool maintainOffset;

    private Quaternion targetRotation;
    private Quaternion restRotation;

    private Vector3 lookForward;
    private Vector3 lookUp;
    void Start()
    {
        restRotation = transform.rotation;
    }

    void LateUpdate()
    {
        Vector3 fwd = target.position - transform.position;
        Vector3 up = upObject.rotation * worldUpAxis;
        Vector3 right = Vector3.Cross(fwd, up);
        up = Vector3.Cross(fwd, right);
        
        if (aimAxis == Vector3.forward)
        {
            lookForward = fwd;
            lookUp = up;
        } else if (aimAxis == Vector3.up)
        {
            lookForward = up;
            lookUp = fwd;
        }
        else
        {
            lookForward = right;
            lookForward = up;
        }

        Quaternion rot = Quaternion.LookRotation(lookForward, lookUp);
        transform.rotation = rot * restRotation;
    }
}
